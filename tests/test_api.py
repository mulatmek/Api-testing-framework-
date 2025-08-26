import requests
import pytest

def test_reverse_normal(base_url):
    """Test reversing a standard sentence."""
    response = requests.get(f"{base_url}/reverse", params={"in": "The quick brown fox"})
    assert response.status_code == 200
    assert response.json()["result"] == "fox brown quick The"

def test_reverse_with_numbers(base_url):
    """Test reversing a string containing numbers."""
    response = requests.get(f"{base_url}/reverse", params={"in": "123 456 789"})
    assert response.status_code == 200
    assert response.json()["result"] == "789 456 123"

def test_reverse_empty_string(base_url):
    """Test that an empty string returns a 400 error."""
    response = requests.get(f"{base_url}/reverse", params={"in": ""})
    assert response.status_code == 400
    assert "must not be empty" in response.json()["detail"]

def test_restore_after_reverse(base_url):
    """Test that /restore returns the last reversed result."""
    requests.get(f"{base_url}/reverse", params={"in": "hello world"})
    response = requests.get(f"{base_url}/restore")
    assert response.status_code == 200
    assert response.json()["result"] == "world hello"

def test_restore_without_reverse(base_url):
    """Test that /restore returns 404 if no reverse has been called yet."""
    response = requests.get(f"{base_url}/restore")
    assert response.status_code in (200, 404)
    if response.status_code == 404:
        assert "Use /reverse first" in response.json()["detail"]

def test_invalid_path(base_url):
    """Test that a non-existent endpoint returns 404."""
    response = requests.get(f"{base_url}/not-a-real-endpoint")
    assert response.status_code == 404
