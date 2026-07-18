"""Step 1: A basic chatbot backed by a local Ollama model.

Sends messages to a locally running Ollama server and keeps the
conversation history so follow-up questions have context.
"""

import sys

import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "gemma4:e4b"


def chat(messages: list[dict[str, str]]) -> str:
    response = requests.post(
        OLLAMA_URL,
        json={"model": MODEL, "messages": messages, "stream": False},
    )
    response.raise_for_status()
    return response.json()["message"]["content"]


def main() -> None:
    print(f"Chatting with {MODEL} via Ollama. Type 'exit' or 'quit' to stop.\n")

    messages: list[dict[str, str]] = []

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if user_input.lower() in {"exit", "quit"}:
            break
        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})

        try:
            reply = chat(messages)
            print(f"{MODEL}: {reply}\n")
            messages.append({"role": "assistant", "content": reply})
        except requests.exceptions.ConnectionError:
            print(
                "Could not reach Ollama at "
                f"{OLLAMA_URL}. Is 'ollama serve' running?",
                file=sys.stderr,
            )
            messages.pop()
            continue

if __name__ == "__main__":
    main()
