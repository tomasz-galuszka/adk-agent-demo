import base64
import io
import logging

import torch
from PIL import Image
from diffusers import StableDiffusionXLInpaintPipeline

logger = logging.getLogger(__name__)

# model ładowany raz
pipe = StableDiffusionXLInpaintPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16,
).to("mps")

# Example callback function
def progress_callback(step: int, timestep: int, latents):
    print(f"Step {step}, Timestep {timestep}")



def edit_image_tool(image_bytes: bytes | str, prompt: str) -> bytes:
    """
        Use this tool to edit an image based on a text prompt.
    """
    logger.info(f"-- {prompt}")
    logger.info(f"-- {image_bytes}")


    if not isinstance(image_bytes, bytes):
        raise TypeError(f"Expected image_bytes as bytes, got {type(image_bytes)}")

    # Load image from raw bytes
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    logger.info(f"-- {image}")
    # Create a white mask (255 = areas to inpaint)
    mask_image = Image.new("L", image.size, 255)

    edited_image_output = pipe(
        prompt=prompt,
        image=image,
        mask_image=mask_image,
        callback=progress_callback,
        callback_steps=1       # callback called every step
    )  # <-- make sure your SD pipeline is called correctly

    # Extract the first image
    edited_image = edited_image_output.images[0]

    # Save to bytes
    output_bytes = io.BytesIO()
    edited_image.save(output_bytes, format="PNG")
    return output_bytes.getvalue()