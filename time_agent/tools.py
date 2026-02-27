import datetime


def get_time(city: str) -> dict:
    """Retrieves the current time for specified city.

    Args:
        city (str): The name of the city (e.g., "New York", "London", "Tokyo").

    Returns:
        dict: A dictionary containing the time information
              Includes a 'status' key ('success' or 'error').
              Includes a 'city' key
              If 'success', includes a 'time' key with time details.
              If 'error', includes an 'error_message' key.
    """

    return {
        "status": "success",
        "city": city,
        "time": f"{datetime.datetime.now().isoformat()}"
    }
