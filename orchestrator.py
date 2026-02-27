from google.adk import Runner
from google.genai import types

from root_agent.agent import root_agent
from sessions import session_service

APP_NAME = "my-agent-app"
USER_ID = "local-user"
SESSION_ID = "local-session-id"

runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service
)


async def call_agent_async(query: str, user_id: str, session_id: str):
    """Sends a query to the agent and prints the final response."""

    content = types.Content(
        role='user',
        parts=[types.Part(text=query)]
    )

    result = "Agent did not produce a final response."  # Default

    async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
        if event.is_final_response():
            if event.content and event.content.parts:
                result = event.content.parts[0].text
            elif event.actions and event.actions.escalate:  # Handle potential errors/escalations
                result = f"Agent escalated: {event.error_message or 'No specific message.'}"
            break

    print(f"<<< Agent Response: {result}")


async def run_conversation(session_id: str, question: str):
    await call_agent_async(query=question, user_id=USER_ID, session_id=session_id)
