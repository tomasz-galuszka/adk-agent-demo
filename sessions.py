from google.adk.sessions import InMemorySessionService

session_service = InMemorySessionService()


async def init_session(app_name: str, user_id: str, session_id: str):
    result = await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id
    )
    print(f"Session created: App='{app_name}', User='{user_id}', Session='{session_id}'")
    return result
