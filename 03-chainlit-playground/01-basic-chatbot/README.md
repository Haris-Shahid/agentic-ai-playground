# 🤖 Basic AI Chatbot with Chainlit

A simple conversational AI chatbot built with **Chainlit**, **OpenAI Agents SDK**, and **Google Gemini (OpenAI Compatible API)**.

This project demonstrates how to build an interactive AI chatbot with a web interface, persistent conversation history, session management, and Google Gemini integration using the OpenAI Agents SDK.

---

## Features

- Interactive chatbot UI using Chainlit
- Google Gemini integration through the OpenAI Compatible API
- OpenAI Agents SDK
- Session-based chat history
- Persistent conversation context
- Async request handling
- Environment variable management with python-dotenv
- UV project management
- Python type hints

---

## Tech Stack

- Python 3.12
- UV
- Chainlit
- OpenAI Agents SDK
- Google Gemini API
- python-dotenv

---

## Project Structure

```
01-basic-chatbot/
│
├── .env.example
├── main.py
├── pyproject.toml
├── uv.lock
└── README.md
```

---

## Prerequisites

Before running this project, make sure you have:

- Python 3.12
- UV package manager
- Google Gemini API Key

### Install Python 3.12 using UV

```bash
uv python install 3.12
```

Verify installed Python versions:

```bash
uv python list
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Haris-Shahid/agentic-ai-playground.git

cd agentic-ai-playground/03-chainlit-playground/01-basic-chatbot
```

---

### 2. Create a virtual environment using Python 3.12

```bash
uv venv --python 3.12
```

---

### 3. Install project dependencies

```bash
uv sync
```

---

### 4. Configure environment variables

Create a `.env` file.

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
```

---

### 5. Run the application

```bash
uv run chainlit run main.py -w
```

The application will be available at:

```
http://localhost:8000
```

---

## What I Learned

During this project, I learned about:

- Building AI chat applications with Chainlit
- OpenAI Agents SDK fundamentals
- Google Gemini OpenAI Compatible API
- Async programming with `async` and `await`
- Session management using `cl.user_session`
- Maintaining conversation history
- Agent configuration with `RunConfig`
- Environment variable management using python-dotenv
- Creating reproducible Python projects with UV

---

## Challenges Faced

### Python 3.14 Compatibility

Initially, this project was created using **Python 3.14**.

While running Chainlit, I encountered runtime errors related to:

- AnyIO
- Event loop handling
- ASGI application startup

After investigating the issue, I recreated the project using **Python 3.12**, which resolved the compatibility problems.

This project is therefore developed and tested with **Python 3.12**.

---

## Useful UV Commands

Install Python 3.12

```bash
uv python install 3.12
```

List installed Python versions

```bash
uv python list
```

Create a virtual environment

```bash
uv venv --python 3.12
```

Install project dependencies

```bash
uv sync
```

Add a package

```bash
uv add package-name
```

Run the application

```bash
uv run chainlit run main.py -w
```

---

## Learning Resources

### UV Documentation

https://docs.astral.sh/uv/

### Chainlit Documentation

https://docs.chainlit.io/

### OpenAI Agents SDK

https://openai.github.io/openai-agents-python/

### Google Gemini OpenAI Compatible API

https://ai.google.dev/gemini-api/docs/openai

---

## License

MIT