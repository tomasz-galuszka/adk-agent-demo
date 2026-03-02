import logging
from pathlib import Path
from typing import Optional

from google.adk.agents.llm_agent import Agent
from google.adk.models import LiteLlm
from google.genai import types

from .search import load_data
from .tools import _search_company_report

logger = logging.getLogger(__name__)

MODEL = 'ollama_chat/llama3.2:latest'
BASE_DIR = Path(__file__).resolve().parent
instruction = (BASE_DIR / "agent_instruction.md").read_text(encoding="utf-8")


def init(callback_context) -> Optional[types.Content]:
    logger.info("Stock report agent initialization started")
    load_data("report.pdf")
    logger.info("Stock report agent initialization finished")

    return None


stock_report_agent = Agent(
    model=LiteLlm(model=MODEL),
    name="stock_report_agent",
    description="Local RAG agent powered by Ollama and ChromaDB.",
    instruction=instruction,
    tools=[_search_company_report],
    before_agent_callback=init
)
