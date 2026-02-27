from dotenv import load_dotenv
from google.adk.agents.llm_agent import Agent

from weather_agent.tools import get_weather

load_dotenv()

MODEL_GOOGLE = 'gemini-2.5-flash'

weather_agent = Agent(
    model=MODEL_GOOGLE,
    name='city_weather_agent',
    description="Provides weather information for specific cities.",
    instruction="You are a helpful weather assistant. "
                "When the user asks for the weather in a specific city, "
                "use the 'get_weather' tool to find the information. "
                "If the tool returns an error, inform the user politely. "
                "If the tool is successful, present the weather report clearly.",
    tools=[get_weather]
)
