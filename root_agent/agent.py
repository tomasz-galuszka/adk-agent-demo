from google.adk.agents.llm_agent import Agent
from google.adk.models import LiteLlm

from time_agent.agent import my_agent
from weather_agent.agent import weather_agent

MODEL = 'ollama_chat/llama3.2:latest'

root_agent = Agent(
    model=LiteLlm(model=MODEL),
    name='city_time_weather_agent',
    description="Main agent: Providers company data based on indexed reports",
    instruction="You are the main Agent. Your job is to provide weather or company data information using subagents."
                "Delegate question question about weather to 'weather_agent' and question about company dataa to 'my_agent'. "
                "Handle only weather and company data related questions. If the question is not related to weather or company data, respond with 'I can only answer questions about weather and company data.'",
    sub_agents=[my_agent, weather_agent],
)
