import os
import pytest
import requests
import time
import subprocess

@pytest.fixture(scope="session")
def base_url():
    """Return the API base URL from environment or default to localhost."""
    return os.getenv("API_BASE_URL", "http://localhost:8000")


# @pytest.fixture(scope="session", autouse=True)
# def docker_container():
#     """Start the application container before tests and shut it down after."""
#     try:
#         subprocess.run(["docker-compose", "up", "--build", "-d"], check=True)
#     except subprocess.CalledProcessError as e:
#         pytest.fail(f"Failed to start Docker container: {e}")
#
#     yield
#
#     subprocess.run(["docker-compose", "down"], check=True)

@pytest.fixture(scope="session", autouse=True)
def wait_for_server(base_url):
    """Wait for the API server to respond to a health check."""

    health_check_url = f"{base_url}/health"
    timeout = 15

    for _ in range(timeout):
        try:
            r = requests.get(health_check_url)
            if r.status_code == 200 and r.json().get("status") == "ok":
                return
        except requests.RequestException:
            pass
        time.sleep(1)

    pytest.fail(f"Server not reachable at {health_check_url} after {timeout} seconds.")
