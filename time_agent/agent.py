from dotenv import load_dotenv
from google.adk.agents.llm_agent import Agent

from time_agent.tools import get_time

load_dotenv()

MODEL_GOOGLE = 'gemini-2.5-flash'

time_agent = Agent(
    model='gemini-2.5-flash',
    name='city_time_agent',
    description="Provides time information for specific cities.",
    instruction="You are a helpful weather assistant. "
                "When the user asks for the time in a specific city, "
                "use the 'get_time' tool to find the information. "
                "If the tool returns an error, inform the user politely. "
                "If the tool is successful, present the city data clearly.",
    tools=[get_time]
)
