import base64
import io
import logging
from pathlib import Path
from typing import Any, Dict, Optional

from PIL import Image
from google.adk.agents.llm_agent import Agent
from google.adk.models import LiteLlm
from google.adk.tools import BaseTool, ToolContext
from google.genai import types

from image_agent.image_tool import edit_image_tool

logger = logging.getLogger(__name__)

MODEL = 'ollama/llava:7b'
BASE_DIR = Path(__file__).resolve().parent
instruction = (BASE_DIR / "agent_instruction.md").read_text(encoding="utf-8")


def init(callback_context) -> Optional[types.Content]:
    print(f"Initializing vision_agent agent with context: {callback_context}")
    return None


def extract(
    tool: BaseTool,
    args: Any,
    tool_context: ToolContext
) -> Optional[Dict]:
    logger.info(f"▶ Intercepting tool: {tool.name}")
    logger.info(f"▶ Intercepting args: {args}")

    prompt = tool_context.user_content.parts[0].text
    blob = tool_context.user_content.parts[1].inline_data

    # blob.data is already bytes
    image_bytes = blob.data

    args["image_bytes"] = image_bytes
    args["prompt"] = prompt

    logger.info(f"▶ Calling tool...")

    # Return None to allow the tool to execute normally
    return None

root_agent = Agent(
    model=LiteLlm(model=MODEL, request_timeout=1800),
    name="vision_agent",
    description="Vision agent that can describe and edit images.",
    instruction=instruction,
    before_agent_callback=init,
    tools=[edit_image_tool],
    before_tool_callback=extract
)
