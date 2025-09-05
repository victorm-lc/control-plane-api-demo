import os
import time

import requests
from dotenv import load_dotenv


load_dotenv()

# required environment variables
CONTROL_PLANE_HOST = os.getenv("CONTROL_PLANE_HOST")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
MAX_WAIT_TIME = 1800  # 30 mins


def get_headers() -> dict:
    """Return common headers for requests to LangGraph Control Plane API."""
    return {
        "X-Api-Key": LANGSMITH_API_KEY,
    }


def list_listeners() -> dict:
    """List all available listeners."""
    response = requests.get(
        f"{CONTROL_PLANE_HOST}/v2/listeners",
        headers=get_headers(),
    )
    
    # Handle non-200 responses
    if response.status_code != 200:
        return {"error": f"HTTP {response.status_code}", "message": response.text}
    
    return response.json()


if __name__ == "__main__":
    print(list_listeners())