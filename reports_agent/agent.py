from dotenv import load_dotenv
from google.adk.agents.llm_agent import Agent
from google.adk.models import LiteLlm

from reports_agent.tools import search_company_report

load_dotenv()
MODEL = 'ollama_chat/llama3.2:latest'

stock_report_agent = Agent(
    model=LiteLlm(model=MODEL),
    name="company_reports_agent",
    description="Local RAG agent powered by Ollama and ChromaDB.",
    instruction=(
        "You are a professional financial assistant.\n\n"
        "RULES:\n"
        "1. If question relates to revenue, profit, annual report, risks, "
        "strategy or management — ALWAYS use tool 'search_company_report'.\n"
        "2. If question relates to current time — use 'get_time'.\n"
        "3. Base answer strictly on tool output when tool is used."
    ),
    tools=[search_company_report]
)
