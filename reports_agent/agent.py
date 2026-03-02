from typing import Optional

from google.adk.agents.llm_agent import Agent
from google.adk.models import LiteLlm
from google.genai import types

from .search import load_data
from .tools import _search_company_report

MODEL = 'ollama_chat/llama3.2:latest'


def init(callback_context) -> Optional[types.Content]:
    load_data("report.pdf")
    return None


stock_report_agent = Agent(
    model=LiteLlm(model=MODEL),
    name="stock_report_agent",
    description="Local RAG agent powered by Ollama and ChromaDB.",
    instruction=(
        "You are a professional financial assistant.\n\n"
        "RULES:\n"
        "1. If question relates to revenue, profit, annual report, risks, "
        "strategy or management — ALWAYS use tool '_search_company_report'.\n"
        "2. If question relates to current time — use 'get_time'.\n"
        "3. Base answer strictly on tool output when tool is used."
    ),
    tools=[_search_company_report],
    before_agent_callback=init
)
