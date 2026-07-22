# 02 - Gemini Agent using OpenAI Agents SDK

This project demonstrates how to build an AI agent using **Google Gemini** with the **OpenAI Agents SDK** by leveraging Gemini's OpenAI-compatible API.

---

## Features

- Build an AI agent using the OpenAI Agents SDK
- Use Google Gemini as the LLM provider
- Load API keys securely with `python-dotenv`
- Configure a custom OpenAI-compatible API endpoint
- Run the agent synchronously

---

## Technologies

- Python
- UV
- OpenAI Agents SDK
- Google Gemini API
- python-dotenv

---

## Project Structure

```text
02_gemini_agent_openai_sdk/
│
├── main.py
├── .env.example
├── pyproject.toml
├── uv.lock
└── README.md
```

---

## Prerequisites

- Python 3.12+
- UV
- Google Gemini API Key

---

## Installation

### Clone Repository

```bash
git clone https://github.com/Haris-Shahid/agentic-ai-playground.git
```

```bash
cd agentic-ai-playground
cd 02_gemini_agent_openai_sdk
```

### Create Virtual Environment

```bash
uv venv
```

### Install Dependencies

```bash
uv sync
```

---

## Environment Variables

Create a `.env` file in the project directory.

```env
GEMINI_API_KEY=your_api_key_here
```

---

## Run the Project

```bash
uv run main.py
```

---

## Code

```python
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-3.6-flash",
    openai_client=client
)

agent = Agent(
    name="Assistant",
    model=model
)

result = Runner.run_sync(
    agent,
    "Welcome and motivate me to learn Agentic AI"
)

print(result.final_output)
```

---

## Learning Resources

### Google Gemini OpenAI Compatibility

https://ai.google.dev/gemini-api/docs/openai

Provides instructions for using the Gemini API with OpenAI-compatible SDKs, including API key generation and the required `base_url`.

---

### OpenAI Agents SDK - Non-OpenAI Models

https://openai.github.io/openai-agents-python/models/

Documentation for integrating third-party models such as Google Gemini with the OpenAI Agents SDK.

---

### UV Documentation

https://docs.astral.sh/uv/getting-started/installation/

Official installation and project management guide for UV.

---

## Expected Output

```text
Agent Response:
Welcome to the exciting world of Agentic AI!
...
```

---

## What's Next

- Configure custom model settings
- Add system instructions
- Use tools with agents
- Build multi-agent workflows
- Explore memory and handoffs

---

## License

MIT