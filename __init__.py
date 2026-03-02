"""
ADK Agent package initialization.
Load environment variables at package level before importing any modules.
"""
import logging

from dotenv import load_dotenv

# This runs when the package is first imported
load_dotenv()

# W __init__.py - na samym początku
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)