# 01 - First AI Agent

This project demonstrates how to build and run your first AI agent using the OpenAI Agents SDK.

---

## Features

- Create an AI agent
- Load API key using python-dotenv
- Run the agent synchronously
- Generate a response using the OpenAI API

---

## Prerequisites

- Python 3.12+
- UV
- OpenAI API Key

---

## Installation

### Clone Repository

```bash
git clone https://github.com/<username>/agentic-ai-playground.git
```

```bash
cd agentic-ai-playground
cd 01-first-agent
```

### Create Virtual Environment

```bash
uv venv
```

### Install Dependencies

```bash
uv sync
```

### Create Environment Variables

Create a `.env` file.

```env
OPENAI_API_KEY=your_api_key_here
```

---

## Run

```bash
uv run main.py
```

---

## Project Structure

```
01-first-agent/
│
├── main.py
├── .env.example
├── pyproject.toml
├── uv.lock
└── README.md
```

---

## Code

```python
from agents import Agent, Runner
from dotenv import load_dotenv

load_dotenv()

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant"
)

result = Runner.run_sync(
    agent,
    "What is AI?"
)

print(result)
```

---

## Learning Resources

### OpenAI API Quickstart

https://developers.openai.com/api/docs/quickstart?desktop-os=windows

### OpenAI Agents SDK

https://developers.openai.com/api/docs/guides/agents

### UV Documentation

https://docs.astral.sh/uv/getting-started/installation/

---

## License

MIT