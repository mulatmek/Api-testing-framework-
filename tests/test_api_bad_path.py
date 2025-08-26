import requests
import pytest
import subprocess
import time

def test_reverse_empty_string(base_url):
    """Error path: empty 'in' should return 400 + helpful detail."""
    response = requests.get(f"{base_url}/reverse", params={"in": ""})
    assert response.status_code == 400
    assert "must not be empty" in response.json()["detail"]


def test_restore_without_reverse(base_url):
    """Error path: /restore before any reverse call."""
    response = requests.get(f"{base_url}/restore")
    assert response.status_code == 404
    assert "Use /reverse first" in response.json()["detail"]


def test_invalid_path(base_url):
    """Error path: non-existent endpoint should return 404."""
    response = requests.get(f"{base_url}/not-a-real-endpoint")
    assert response.status_code == 404


def test_server_crash_between_calls(base_url):
    """Simulate a crash using docker compose, then verify recovery."""
    # 1) Normal reverse
    r1 = requests.get(f"{base_url}/reverse", params={"in": "hello world"})
    assert r1.status_code == 200
    assert r1.json()["result"] == "world hello"

    # 2) Crash the service (kill container)
    subprocess.run(["docker-compose", "down"], check=True)

    # 3) While down, requests should fail
    with pytest.raises(requests.exceptions.RequestException):
        requests.get(f"{base_url}/restore", timeout=2)

    # 4) Bring it back
    subprocess.run(["docker-compose", "up", "--build", "-d"], check=True)

    # 5) Wait until it's reachable again
    deadline = time.time() + 30
    while time.time() < deadline:
        try:
            r = requests.get(f"{base_url}/health", timeout=2)
            if r.status_code == 200:
                break
        except requests.RequestException:
            pass
        time.sleep(1)

    r2 = requests.get(f"{base_url}/restore")
    assert r2.status_code == 404
    assert "Use /reverse first" in r2.json()["detail"]
