import os
import json
import urllib.request
import urllib.error


def call_with_sdk():
    try:
        from openai import OpenAI
    except ImportError:
        print("Install the SDK: pip install openai")
        return

    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=256,
        messages=[{"role": "user", "content": "What is a neural network in one sentence?"}]
    )
    print(f"SDK response: {response.choices[0].message.content}")
    print(f"Tokens used: {response.usage.prompt_tokens} in, {response.usage.completion_tokens} out")


def call_raw_http():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Set OPENAI_API_KEY environment variable first")
        return

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    body = json.dumps({
        "model": "gpt-4o-mini",
        "max_tokens": 256,
        "messages": [{"role": "user", "content": "What is a neural network in one sentence?"}],
    }).encode()

    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
            print(f"Raw HTTP response: {result['choices'][0]['message']['content']}")
            print(f"Tokens used: {result['usage']['prompt_tokens']} in, {result['usage']['completion_tokens']} out")
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"Error {e.code}: {body}")


if __name__ == "__main__":
    print("=== OpenAI API Calls ===\n")
    print("1. Using the SDK:")
    call_with_sdk()
    print("\n2. Using raw HTTP:")
    call_raw_http()
