import asyncio

from orchestrator import run_conversation, APP_NAME, USER_ID, SESSION_ID
from sessions import init_session

if __name__ == "__main__":
    try:
        session = asyncio.run(init_session(APP_NAME, USER_ID, SESSION_ID))
        asyncio.run(run_conversation(question="What is the weather like in London?", session_id=session.id))
        asyncio.run(run_conversation(question="What is the time in London?", session_id=session.id))
    except Exception as e:
        print(f"An error occurred: {e}")
