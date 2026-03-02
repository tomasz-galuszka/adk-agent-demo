"""
ADK Agent package initialization.
Load environment variables at package level before importing any modules.
"""
from dotenv import load_dotenv

# This runs when the package is first imported
load_dotenv()

