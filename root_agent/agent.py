import logging
from pathlib import Path
from typing import Optional

from google.adk.agents import LlmAgent
from google.adk.agents.llm_agent import Agent
from google.adk.models import LiteLlm
from google.genai import types

from reports_agent import stock_report_agent

logger = logging.getLogger(__name__)

MODEL = 'ollama_chat/llama3.2:latest'
BASE_DIR = Path(__file__).resolve().parent
instruction = (BASE_DIR / "agent_instruction.md").read_text(encoding="utf-8")

def init_root_agent(callback_context) -> Optional[types.Content]:
    logger.info(f"Root agent initialization finished: {callback_context}")
    return None


root_agent: LlmAgent = Agent(
    model=LiteLlm(model=MODEL),
    name='root_agent',
    description="Main agent: Provide stock company analysis and data based on dedicated subagents.",
    instruction=instruction,
    sub_agents=[stock_report_agent],
    before_agent_callback=init_root_agent
)
