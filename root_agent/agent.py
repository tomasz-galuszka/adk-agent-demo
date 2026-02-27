from google.adk.agents.llm_agent import Agent
from google.adk.models import LiteLlm

from time_agent.agent import time_agent
from weather_agent.agent import weather_agent

MODEL = 'ollama_chat/llama3.2:latest'

root_agent = Agent(
    model=LiteLlm(model=MODEL),
    name='city_time_weather_agent',
    description="Main agent: Provides weather or time in cities",
    instruction="You are the main Weather and Time Agent. Your job is to provide weather or time using your subagents "
                "Delegate question about time in cities to 'time_agent' and question about weather to 'weather_agent'. "
                "Handle only weather and time requests in cities",
    sub_agents=[time_agent, weather_agent],
)
