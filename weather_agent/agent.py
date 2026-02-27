from dotenv import load_dotenv
from google.adk.agents.llm_agent import Agent
from google.adk.models import LiteLlm

from weather_agent.tools import get_weather
import litellm

load_dotenv()

MODEL = 'ollama_chat/llama3.2:latest'

weather_agent = Agent(
    model=LiteLlm(model=MODEL),
    name='city_weather_agent',
    description="Provides weather information for specific cities.",
    instruction="You are a helpful weather assistant. "
                "When the user asks for the weather in a specific city, "
                "use the 'get_weather' tool to find the information. "
                "If the tool returns an error, inform the user politely. "
                "If the tool is successful, present the weather report clearly.",
    tools=[get_weather]
)
