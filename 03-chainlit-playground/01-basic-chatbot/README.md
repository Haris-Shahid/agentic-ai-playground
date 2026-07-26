# 🤖 Basic AI Chatbot with Chainlit

A simple conversational AI chatbot built with **Chainlit**, **OpenAI Agents SDK**, and **Google Gemini (OpenAI Compatible API)**.

This project demonstrates how to build an interactive AI chatbot with persistent conversation history using the OpenAI Agents SDK inside a Chainlit application.

---

## Features

- Interactive chatbot UI using Chainlit
- Google Gemini integration via OpenAI Compatible API
- OpenAI Agents SDK
- Session-based chat history
- Persistent conversation context
- Environment variable management with python-dotenv
- UV project management

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
├── .env
├── main.py
├── pyproject.toml
├── uv.lock
└── README.md
```

---

## Installation

### Clone the repository

```bash
git clone https://github.com/Haris-Shahid/agentic-ai-playground.git

cd agentic-ai-playground/03-chainlit-playground/01-basic-chatbot
```

---

### Create the virtual environment

```bash
uv python install 3.12
uv venv --python 3.12
```

---

### Install dependencies

```bash
uv sync
```

---

### Configure environment variables

Create a `.env` file.

```env
GEMINI_API_KEY=YOUR_API_KEY
BASE_URL=your_gemini_base_url_for_openai
```

---

### Run the application

```bash
uv run chainlit run main.py -w
```

---

## Learning Outcomes

This project helped me learn:

- Building conversational AI applications
- Chainlit event lifecycle
- Session management
- OpenAI Agents SDK
- Async programming
- RunConfig
- Conversation history management
- Gemini OpenAI Compatible API

---

## Challenges Faced

### Python 3.14 Compatibility

While building this project, I encountered runtime issues with:

- Chainlit
- AnyIO
- Event loop handling

The project worked correctly after switching from:

```
Python 3.14
```

to

```
Python 3.12
```

which is currently a more stable version for this stack.

---

## Resources

### UV

https://docs.astral.sh/uv/

### Chainlit

https://docs.chainlit.io/

### OpenAI Agents SDK

https://openai.github.io/openai-agents-python/

### Google Gemini OpenAI Compatibility

https://ai.google.dev/gemini-api/docs/openai

---

## License

MIT