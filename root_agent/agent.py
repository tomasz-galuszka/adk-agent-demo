from google.adk.agents.llm_agent import Agent
from google.adk.models import LiteLlm

from reports_agent.agent import stock_report_agent

MODEL = 'ollama_chat/llama3.2:latest'

root_agent = Agent(
    model=LiteLlm(model=MODEL),
    name='root_financial_agent',
    description="Main agent: Providers stock company analysis and data based on indexed reports.",
    instruction="You are the main Agent. Your job is to provide stock companies data and analysis information using specialized subagents."
                "You can describe what you can do by saying 'I can provide stock company data and analysis based on indexed reports.'"
                "Please answer on questions in human readable format. If you don't know the answer, say you don't know. Always try to use subagents if the question is related to stock companies."
                "Delegate question about stock company data and analysis to 'stock_report_agent'."
                "Handle only questions related to stock companies. If the question is not related to stick companies respond with 'I can only answer questions about stock companies.'",
    sub_agents=[stock_report_agent]
)
