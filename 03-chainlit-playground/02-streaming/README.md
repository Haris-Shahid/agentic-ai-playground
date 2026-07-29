# 🤖 Streaming AI Chatbot with Chainlit

A conversational AI chatbot built with **Chainlit**, the **OpenAI Agents SDK**, and **Google Gemini through its OpenAI-compatible API**.

This project demonstrates how to stream AI responses token by token while maintaining session-based conversation history.

---

## Features

- Interactive chatbot UI built with Chainlit
- Token-by-token AI response streaming
- Google Gemini integration through the OpenAI-compatible API
- OpenAI Agents SDK integration
- Session-based chat history using `cl.user_session`
- Persistent multi-turn conversation context
- Asynchronous event handling
- Streaming with `Runner.run_streamed()`
- Real-time token display using `msg.stream_token()`
- Environment variable management using `python-dotenv`
- API key and base URL validation
- UV-based Python and dependency management

---

## Tech Stack

- Python 3.12
- UV
- Chainlit
- OpenAI Agents SDK
- Google Gemini API
- OpenAI-compatible API
- python-dotenv

---

## Project Structure

```text
02-streaming-chatbot/
│
├── .env.example
├── .python-version
├── README.md
├── chainlit.md
├── main.py
├── pyproject.toml
└── uv.lock
```

> The `.env` file is not included because it contains sensitive API credentials.

---

## How Streaming Works

The application uses `Runner.run_streamed()` to receive the AI response incrementally instead of waiting for the complete response.

Each response token is:

1. Received through `result.stream_events()`
2. Added to `response_content`
3. Displayed immediately in the Chainlit UI using `msg.stream_token()`
4. Combined into the complete assistant response
5. Saved to the conversation history after streaming is complete

### Streaming Flow

```text
User Message
      ↓
Add User Message to Chat History
      ↓
Runner.run_streamed()
      ↓
Receive Stream Events
      ↓
Display Tokens in Chainlit
      ↓
Build Complete Response
      ↓
Save Assistant Response to Chat History
      ↓
Store Updated History in User Session
```

## Prerequisites

Before running this project, install:

- Python 3.12 or let UV manage the Python installation
- UV
- A Google Gemini API key

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Haris-Shahid/agentic-ai-playground.git
```

### 2. Navigate to the project

```bash
cd agentic-ai-playground/03-chainlit-playground/02-streaming-chatbot
```

### 3. Install Python 3.12 using UV

If Python 3.12 is not already available on your system, install it with:

```bash
uv python install 3.12
```

### 4. Install the project dependencies

```bash
uv sync
```

`uv sync` installs the dependencies defined in `pyproject.toml` and creates or updates the project's virtual environment when required.

---

## Creating a New UV Project with Python 3.12

To create a new UV project directly with Python 3.12:

```bash
uv init --python 3.12 my-project
```

For example:

```bash
uv init --python 3.12 02-streaming-chatbot
```

Then enter the project directory:

```bash
cd 02-streaming-chatbot
```

Add the required dependencies:

```bash
uv add chainlit
uv add openai-agents
uv add python-dotenv
```

Synchronize the project:

```bash
uv sync
```

This setup ensures that the project is configured to use Python 3.12 from the beginning.

---

## Switching an Existing UV Project from Python 3.14 to Python 3.12

If you accidentally created a project using the latest Python version, such as Python 3.14, and a package has compatibility issues, you can switch the project to Python 3.12.

### 1. Check the current Python version

Run:

```bash
uv run python --version
```

Example output:

```text
Python 3.14.6
```

### 2. Install Python 3.12

```bash
uv python install 3.12
```

### 3. Update the project's Python requirement

Open `pyproject.toml` and change:

```toml
requires-python = ">=3.14"
```

to:

```toml
requires-python = ">=3.12"
```

If the project already supports a wider Python range, keep the requirement appropriate for the dependencies used by the project.

### 4. Recreate the virtual environment with Python 3.12

Delete the existing virtual environment.

Windows PowerShell:

```powershell
Remove-Item -Recurse -Force .venv
```

Windows Command Prompt:

```cmd
rmdir /s /q .venv
```

Then create the environment using Python 3.12:

```bash
uv venv --python 3.12
```

### 5. Synchronize the dependencies

```bash
uv sync
```

UV will install the dependencies into the new Python 3.12 environment.

### 6. Verify the Python version

Run:

```bash
uv run python --version
```

Expected output:

```text
Python 3.12.x
```

### 7. Run the application

```bash
uv run chainlit run main.py -w
```

---

## Alternative: Use UV to Change the Project Python Version

You can also use:

```bash
uv python pin 3.12
```

This updates the project's `.python-version` file to use Python 3.12.

Then run:

```bash
uv sync
```

Verify the active Python version:

```bash
uv run python --version
```

Expected output:

```text
Python 3.12.x
```

> If UV continues using the old virtual environment, delete `.venv` and run `uv sync` again.

---

## Environment Variables

Create a `.env` file in the project directory:

```env
GEMINI_API_KEY=your_gemini_api_key
BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
```

Do not commit your `.env` file because it contains your private API key.

The `.env.example` file can be committed because it contains only placeholder values.

Example `.env.example`:

```env
GEMINI_API_KEY=your_gemini_api_key
BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
```

---

## Run the Application

Run:

```bash
uv run chainlit run main.py -w
```

Then open:

```text
http://localhost:8000
```

The `-w` flag enables watch mode, so Chainlit automatically reloads the application when code changes are detected.

---

## Learning Outcomes

This project helped me learn:

- Building interactive AI applications with Chainlit
- Chainlit lifecycle events
- `@cl.on_chat_start`
- `@cl.on_message`
- Session management using `cl.user_session`
- Maintaining multi-turn conversation history
- Persistent conversation context
- Asynchronous Python programming
- `async` and `await`
- Asynchronous iteration using `async for`
- Streaming AI responses with `Runner.run_streamed()`
- Processing streaming events with `result.stream_events()`
- Displaying tokens in real time with `msg.stream_token()`
- Collecting the complete streamed response
- Saving assistant responses to chat history
- Using `RunConfig`
- Integrating Google Gemini through an OpenAI-compatible API
- Managing environment variables with `python-dotenv`
- Using `typing.cast` for type checking
- Managing Python versions with UV
- Creating UV projects with a specific Python version
- Switching an existing UV project from Python 3.14 to Python 3.12

---

## Python Compatibility Note

This project was developed using **Python 3.12**.

During development, Python 3.14 caused compatibility and runtime issues with parts of the application stack, including:

- Chainlit
- AnyIO
- Async event-loop behavior

The project worked correctly after switching to Python 3.12.

For this project, Python 3.12 provides a more stable environment for the current dependency stack.

---

## Resources

### UV

https://docs.astral.sh/uv/

### UV Python Versions

https://docs.astral.sh/uv/guides/install-python/

### Chainlit

https://docs.chainlit.io/

### OpenAI Agents SDK

https://openai.github.io/openai-agents-python/

### OpenAI Agents SDK Streaming

https://openai.github.io/openai-agents-python/streaming/

### Google Gemini OpenAI Compatibility

https://ai.google.dev/gemini-api/docs/openai

---

## License

MIT