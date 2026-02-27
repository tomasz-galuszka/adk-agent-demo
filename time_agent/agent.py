import chromadb
from dotenv import load_dotenv
from google.adk.agents.llm_agent import Agent
from google.adk.models import LiteLlm

from time_agent.tools import get_time

load_dotenv()

MODEL = 'ollama_chat/llama3.2:latest'

chroma_client = chromadb.HttpClient(host='localhost', port=8000)
collections = chroma_client.list_collections()
print(collections)

time_agent = Agent(
    model=LiteLlm(model=MODEL),
    name='city_time_agent',
    description="Provides the current time information for specific city.",
    instruction="You are a helpful weather assistant. "
                "When the user asks for the current time in a specific city, "
                "use the 'get_time' tool to find and return the information. "
                "If the tool returns an error, inform the user politely. "
                "If the tool is successful, present the time clearly.",
    tools=[get_time]
)
