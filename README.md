# AI Agent Calculator

A production-ready **AI Assistant** capable of intelligently routing user queries between **Mathematical Reasoning**, **Real-Time Web Search**, and **General Knowledge**. Built with a focus on security, observability, and modern "Full-Stack" AI architecture.

<img src="https://i.imgur.com/FKgSYYa.png" alt="PaDiM Demo" width="100%" height="50%">

---

## Architecture & Design Decisions

This project implements the **ReAct (Reasoning + Acting)** pattern. Instead of relying on opaque function calling, the agent explicitly reasons about which tool to use, making the logic transparent and auditable.

### 🛠 Tech Stack
*   **Orchestration:** [LangChain](https://www.langchain.com/) (Python).
*   **Inference (LLM):** **Llama-3.3-70b-versatile** via Groq API.
    *   *Engineering Decision:* Llama 3.3 was selected for its superior reasoning capabilities and ultra-low latency on Groq's LPUs, essential for a responsive agentic workflow.
*   **Tools:**
    *   **Calculator:** Implemented using `numexpr` to sanitize inputs and prevent **Arbitrary Code Execution (ACE)** vulnerabilities common with Python's `eval()`.
    *   **Search:** Integrated **Tavily API** (optimized for LLMs) to ensure reliable, structured data retrieval, replacing unstable scraping methods.
*   **Interface:** [Streamlit](https://streamlit.io/) for a chat-based Web UI.
*   **Dependency Management:** [Poetry](https://python-poetry.org/) for deterministic builds.

### Logic Flow (The Router)
1.  **Input:** User sends a prompt (e.g., *"What is the USD to BRL exchange rate?"*).
2.  **Reasoning:** The Agent analyzes intent based on strict System Prompt rules.
3.  **Routing:**
    *   If **Math** $\rightarrow$ Invokes `calculator_tool`.
    *   If **Real-Time Info** $\rightarrow$ Invokes `tavily_search`.
    *   If **General Chat** $\rightarrow$ Responds directly (bypassing tools).
4.  **Execution:** The tool performs the action safely.
5.  **Synthesis:** The LLM interprets the result and formulates the natural language answer.

---

## Project Structure

```text
ai-agent-calculator/
├── src/
│   ├── agent.py       # ReAct Agent definition and Prompt Engineering
│   ├── app.py         # Streamlit Web Interface (Frontend)
│   ├── main.py        # CLI Interface (Backend/Debug)
│   └── tools.py       # Tool definitions (Math & Search)
├── tests/
│   ├── test_agent.py  # Prompt integrity and initialization tests
│   └── test_tools.py  # Unit tests for tools and security
├── .env               # API Keys (GitIgnored)
├── pyproject.toml     # Dependencies
└── README.md          # Documentation
```

---

## How to Run

### Prerequisites
*   Python 3.10+ (Tested on **Python 3.13**).
*   **Poetry** installed.
*   API Keys for **Groq** and **Tavily**.

### 1. Installation
Clone the repository and install dependencies:

```bash
# Clone repository
git clone <YOUR_REPO_URL>
cd ai-agent-calculator

# Install dependencies (sync ensures a clean environment)
poetry install --sync
```

### 2. Configuration
Create a `.env` file in the root directory:

```env
GROQ_API_KEY=gsk_your_groq_key
TAVILY_API_KEY=tvly_your_tavily_key
```

### 3. Execution Modes

#### 🖥️ Web Interface (Recommended)
Runs a modern Chat UI (Gemini-style). The agent's reasoning steps ("Thinking...") are visualized in collapsible containers for a clean user experience.

```bash
poetry run streamlit run src/app.py
```

#### ⌨️ CLI (Terminal)
Runs the agent in the terminal with verbose logging. Ideal for debugging the ReAct loop and seeing raw tool outputs.

```bash
poetry run python -m src.main
```

---

## Quality Assurance

The project includes a robust test suite using `pytest`.

*   **Security:** Validates that code injection attempts (e.g., `import os`) are blocked.
*   **Robustness:** Ensures the calculator handles edge cases (e.g., division by zero).
*   **Prompt Integrity:** Static analysis ensures critical safety rules are present in the system prompt.

**To run tests:**

```bash
poetry run pytest -v
```

> **Current Status:** 100% Pass Rate (12/12 Tests).

---

## Learnings & Evolution

### Challenges & Solutions

1.  **Python 3.14 Compatibility:**
    *   *Issue:* Initial attempts to run on the experimental Python 3.14 caused `Pydantic V1` compatibility errors within LangChain.
    *   *Solution:* Downgraded the environment to a stable **Python 3.13** and configured Poetry with `package-mode = false` to treat the project as an application, ensuring stability.

2.  **Search Tool Instability:**
    *   *Issue:* Initial prototypes using `DuckDuckGo` scraping were inconsistent and prone to rate limits.
    *   *Solution:* Migrated to **Tavily API**, a search engine optimized for AI agents, providing reliable context for real-time queries.

3.  **"Action: None" Loop:**
    *   *Issue:* The model would occasionally get stuck trying to call "None" as a tool for general chat.
    *   *Solution:* Implemented explicit **Prompt Engineering** rules instructing the model to bypass the "Action" step for general greetings, validated by the `test_agent_prompt_engineering` unit test.
