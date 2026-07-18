"""Step 1: A basic chatbot backed by a local Ollama model.

Sends messages to a locally running Ollama server and keeps the
conversation history so follow-up questions have context.
"""

import ast
import operator
import sys
import urllib
import json

import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "gemma4:e4b"

MAX_ITERATIONS = 5

FORMAT = {
    "type": "object",
    "properties": {
        "tool": {"type": "string"},
        "response": {"type": "string"}
    },
    "required": ["tool", "response"]
}

CONTEXT = """
# Output format
Send responses always in a fixed JSON schema. Respond with just the json *do not* add additional formatting like markdown or other.

## Example:
Correct output
{
    "tool": "none",
    "response": "How are you today?"
}

Wrong output
```json
{
    "tool": "none",
    "response": "How are you today?"
}
```

# Schema
{
    "tool": "..." // name of the tool that should be called or "none"
    "response": "..." // the final answer or the parameters for the tool call
}
"""

TOOLS = [
    """
    # Calculator (tool = "calculator")
    To evaluate mathematical expressions choose this tool.

    Example:
    __Prompt__: What is ten times four?
    __Response__:
    {
        "tool": "calculator",
        "response": [10, 4]
    }
    """,
    """
    # Wikipedia Search (tool = "wikipedia")
    To gain more knowledge about a specific topic you can search Wikipedia articles with this tool.

    Example
    __Prompt__: Why does a tiger has stripes?
    {
     "tool": "wikipedia",
     "response": "tiger stripes"
    }
    """
]

WIKIPEDIA_AGENT = {"user-agent": "Learning Project/0.1 (https://github.com/JNK90/ai-playground)"}

_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}


def _eval_node(node: ast.AST) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPERATORS:
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        return _ALLOWED_OPERATORS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPERATORS:
        return _ALLOWED_OPERATORS[type(node.op)](_eval_node(node.operand))
    raise ValueError(f"Unsupported expression: {ast.dump(node)}")

def calculate(expression: str) -> str:
    """Evaluate a math expression and return the result as a string.

    Example: calculate("15 * 45") -> "675"
    """
    tree = ast.parse(expression, mode="eval")
    result = _eval_node(tree.body)
    return str(result)

def search_wikipedia(query: str) -> str:
    url_safe_query = urllib.parse.quote_plus(query)
    response = requests.get(f"https://en.wikipedia.org/w/rest.php/v1/search/page?q={url_safe_query}&limit=5", headers=WIKIPEDIA_AGENT)
    summaries = []
    for page in response.json()['pages']:
        summary = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{page['key']}", headers=WIKIPEDIA_AGENT)
        asJson = summary.json()
        summaries.append(f"{asJson['titles']['normalized']} - {asJson['extract']}")
    return "\n".join(summaries)

def executor(tool: str, payload: str) -> str:
    if (tool == 'calculator'):
        return calculate(payload)
    elif (tool == 'wikipedia'):
        return search_wikipedia(payload)
    else:
        raise Exception('Unsupported tool')

def call_model(messages: list[dict[str, str]]) -> str:
    response = requests.post(
        OLLAMA_URL,
        json={"model": MODEL, "messages": messages, "stream": False, "format": FORMAT},
    )
    response.raise_for_status()
    return json.loads(response.json()['message']['content'])

def chat(messages: list[dict[str, str]]) -> str:
    response = call_model(messages)
    iteration = 0
    while (response['tool'] != 'none'):
        result = executor(response['tool'], response['response'])
        messages.append({"role": "assistant", "content": json.dumps(response)})
        messages.append({"role": "user", "content": f"Observation: {result}"})
        response = call_model(messages)
        iteration += 1
        if (iteration >= MAX_ITERATIONS):
            break
    return response['response']
        

def main() -> None:
    print(f"Chatting with {MODEL} via Ollama. Type 'exit' or 'quit' to stop.\n")

    messages: list[dict[str, str]] = [
        {"role": "system", "content": CONTEXT}
    ]
    for tool in TOOLS:
        messages.append({"role": "system", "content": tool})


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
