from pathlib import Path
from typing import Optional

from google.adk.agents.llm_agent import Agent
from google.adk.models import LiteLlm
from google.genai import types

MODEL = 'ollama/llava:7b'
BASE_DIR = Path(__file__).resolve().parent
instruction = (BASE_DIR / "agent_instruction.md").read_text(encoding="utf-8")


def init(callback_context) -> Optional[types.Content]:
    print(f"Initializing vision_agent agent with context: {callback_context}")
    return None

root_agent = Agent(
    model=LiteLlm(model=MODEL),
    name="vision_agent",
    description="Vision agent that describes uploaded images.",
    instruction=instruction,
    before_agent_callback=init
)
