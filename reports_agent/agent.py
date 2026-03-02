from typing import Optional

from dotenv import load_dotenv
from google.adk.agents.callback_context import CallbackContext
from google.adk.agents.llm_agent import Agent
from google.adk.models import LiteLlm
from google.genai import types  # For types.Content

from reports_agent.tools import search_company_report
from search.db import chroma_client
from search.index_loader import load_data

MODEL = 'ollama_chat/llama3.2:latest'
load_dotenv()

def init(callback_context) -> Optional[types.Content]:
    collection = chroma_client.get_or_create_collection(name="company_reports")
    load_data(collection, "report.pdf")
    return None

stock_report_agent = Agent(
    model=LiteLlm(model=MODEL),
    name="stock_report_agent",
    description="Local RAG agent powered by Ollama and ChromaDB.",
    instruction=(
        "You are a professional financial assistant.\n\n"
        "RULES:\n"
        "1. If question relates to revenue, profit, annual report, risks, "
        "strategy or management — ALWAYS use tool 'search_company_report'.\n"
        "2. If question relates to current time — use 'get_time'.\n"
        "3. Base answer strictly on tool output when tool is used."
    ),
    tools=[search_company_report],
    before_agent_callback=init
)
