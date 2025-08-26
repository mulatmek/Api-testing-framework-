import pytest
import requests

@pytest.mark.parametrize(
    "input_text, expected",
    [
        ("The quick brown fox", "fox brown quick The"),
        ("123 456 789", "789 456 123"),
        ("hello world", "world hello"),
        ("single", "single"),  # single word
        ("multiple   spaces here", "here spaces multiple"),  # extra spaces collapse
        ("a b c d e", "e d c b a"),  # short sequence
        ("Python pytest FastAPI test", "test FastAPI pytest Python"),  # longer sentence
        ("¡Hola mundo!", "mundo! ¡Hola"),  # Spanish
        ("こんにちは 世界", "世界 こんにちは"),  # Japanese
        ("שלום עולם", "עולם שלום"),  # Hebrew
    ],
)
def test_reverse(base_url, input_text, expected):
    """Happy path: /reverse returns correct reversed text."""
    response = requests.get(f"{base_url}/reverse", params={"in": input_text})
    assert response.status_code == 200
    assert response.json()["result"] == expected


def test_restore_after_reverse(base_url):
    """Happy path: /restore returns the last reversed result."""
    requests.get(f"{base_url}/reverse", params={"in": "hello world"})
    response = requests.get(f"{base_url}/restore")
    assert response.status_code == 200
    assert response.json()["result"] == "world hello"

def test_reverse_long_string(base_url):
    long_text = "word " * 100_000
    response = requests.get(f"{base_url}/reverse", params={"in": long_text})
    assert response.status_code == 200