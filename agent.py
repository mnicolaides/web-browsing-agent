import os
import sys
import requests
from bs4 import BeautifulSoup
from anthropic import Anthropic

client = Anthropic()

def fetch_webpage(url: str) -> str:
    """Fetch and extract text content from a webpage."""
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; WebAgent/1.0)"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        # Remove scripts and styles
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        text = soup.get_text(separator="\n", strip=True)
        # Truncate to avoid token limits
        return text[:8000]
    except Exception as e:
        return f"Error fetching page: {e}"


tools = [
    {
        "name": "fetch_webpage",
        "description": "Fetches the content of a webpage given its URL and returns the text.",
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "The full URL of the webpage to fetch."}
            },
            "required": ["url"],
        },
    }
]


def run_agent(user_request: str):
    """Run the web browsing agent in an agentic loop."""
    print(f"\n🤖 Agent starting...\nTask: {user_request}\n")
    messages = [{"role": "user", "content": user_request}]

    while True:
        response = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=2048,
            tools=tools,
            messages=messages,
        )

        # Append assistant response
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            # Extract and print final text
            for block in response.content:
                if hasattr(block, "text"):
                    print("📝 Summary:\n")
                    print(block.text)
            break

        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"🌐 Fetching: {block.input['url']}")
                    result = fetch_webpage(block.input["url"])
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                    })
            messages.append({"role": "user", "content": tool_results})


if __name__ == "__main__":
    if len(sys.argv) < 2:
        task = input("What would you like me to research and summarize? ")
    else:
        task = " ".join(sys.argv[1:])
    run_agent(task)
