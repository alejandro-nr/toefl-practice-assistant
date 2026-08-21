from toefl_writing_prep.api_client import OpenRouterClient


def test_client_initialization():
    api_key = "test-secret-key"
    client = OpenRouterClient(api_key=api_key)

    assert client.api_key == api_key
    assert (
        OpenRouterClient.COMPLETIONS_URL
        == "https://openrouter.ai/api/v1/chat/completions"
    )
    assert client.api_url == OpenRouterClient.COMPLETIONS_URL

    api_url = "test-url"
    client = OpenRouterClient(api_key=api_key, api_url=api_url)
    assert client.api_url == api_url


def test_client_headers():
    api_key = "test-secret-key"
    client = OpenRouterClient(api_key=api_key)

    expected_headers = {
        "Authorization": "Bearer test-secret-key",
        "Content-Type": "application/json",
    }

    assert client.headers == expected_headers
