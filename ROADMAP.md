# 🗺️ Roadmap: Learning Agentic Coding
**Goal:** Transition from "AI as a Chatbot" to "AI as an Autonomous Agent."

## 🎯 Project 1: The ReAct Calculator & Wikipedia Agent
**Concept:** Build an agent that uses a "Reasoning and Acting" (ReAct) loop. It doesn't just guess answers; it decides which tool to use, executes it, looks at the result, and decides if it needs to do more work.

### 🛠️ Technical Stack
*   **Language:** Python (The industry standard for AI).
*   **Brain (LLM):** Local model via [Ollama](https://ollama.com) (`gemma4:e4b`), not a remote hosted API. Chosen for simplicity and to avoid API costs while learning. *Note: tool-calling support/format may differ from hosted "Native Tool Calling" models — revisit this in Step 3.*
*   **Tools Library:** `wikipedia-api` (for research) and Python's built-in `eval()` or a math library (for calculation).
*   **Orchestration:** Manual loop implementation (to learn the fundamentals before using frameworks like LangGraph).

---

### 📝 The Development Roadmap

#### **Step 1: The "Dumb" Chatbot (Foundation)**
*   [x] Set up a Python environment (local Ollama server running `gemma4:e4b`, no API keys needed).
*   [x] Write a script that sends a message to an LLM and prints the response.
*   [x] Implement "Memory": Allow the user to ask follow-up questions so the agent remembers the previous turn.
*   Code: `src/step1/chatbot.py`

#### **Step 2: The "Hands" (Tool Definition)**
*   [x] Create a Python function `calculate(expression)` that takes a string and returns a math result.
*   [x] Create a Python function `search_wikipedia(query)` that returns a short summary of a topic.
*   [x] **Crucial Step:** Define these functions in a way that the LLM can "see" them (using JSON Schema or Docstrings).

#### **Step 3: The "Brain" (Tool Calling Logic)**
*   [ ] Implement **Native Tool Calling**: Instead of just text, instruct the LLM to output a `tool_call` object.
*   [ ] Create the **Executor**: Write the logic that:
    1.  Sees the LLM wants to use `calculate`.
    2.  Extracts the math expression from the LLM's request.
    3.  Runs the actual Python function.
    4.  Captures the result.

#### **Step 4: The "Loop" (The Agentic Core)**
*   [ ] Implement the **ReAct Loop**:
    *   **Input:** User asks a question.
    *   **Thought/Action:** LLM decides to use a tool.
    *   **Observation:** Your code runs the tool and gets a result.
    *   **Feedback:** The result is fed *back* into the LLM as a new message.
    *   **Termination:** The loop continues until the LLM provides a "Final Answer" instead of a tool call.

#### **Step 5: Testing "Agentic" Behavior**
*   [ ] **Test Case A (Single Tool):** "What is 15 * 45?" (Should trigger `calculate`).
*   [ ] **Test Case B (Multi-step Reasoning):** "Who is the president of France and what is their age multiplied by 2?"
    *   *Expected Flow:* Search Wiki for President $\rightarrow$ Find Age $\rightarrow$ Use Calculator on Age $\times$ 2 $\rightarrow$ Final Answer.

---

### 🧠 Key Concepts to Master During This Project
1.  **System Prompting:** How to tell an AI "You are an agent with tools."
2.  **JSON Schema:** How to describe functions so an AI understands them.
3.  **The Feedback Loop:** The logic of feeding `Tool Output` back into the `Conversation History`.
4.  **Error Handling:** What happens if the user asks for something impossible? (Does the agent crash, or does it explain why?)