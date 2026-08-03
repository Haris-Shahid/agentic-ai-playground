# 🧠 Context-Aware AI Agents

A hands-on project demonstrating how to pass **typed, application-managed runtime context** to AI agents and function tools using the **OpenAI Agents SDK**.

This project explores how runtime context can be used to:

* Generate personalized agent instructions
* Access user-specific data inside function tools
* Keep selected application data hidden from the LLM
* Execute asynchronous context-aware tools
* Maintain mutable state during the current application runtime
* Share the same context object across multiple agent runs

The project uses **Google Gemini** through its **OpenAI-compatible API**.

---

## 🎯 Project Objectives

The main goal of this project is to understand how an application can provide runtime data to an AI agent without placing all application data directly inside the user's prompt.

The project demonstrates the following concepts:

1. Typed runtime context
2. `RunContextWrapper`
3. Dynamic agent instructions
4. Context-aware function tools
5. Controlled LLM data exposure
6. Asynchronous tools
7. Mutable runtime state
8. Context sharing across multiple agents
9. Runtime context versus persistent memory

---

## 🛠️ Tech Stack

* Python 3.14
* UV
* OpenAI Agents SDK
* Google Gemini API
* OpenAI-compatible API
* `python-dotenv`
* `dataclasses`
* `asyncio`

---

## 📂 Project Structure

```text
02-context-aware-agents/
│
├── .env                 # Local environment variables
├── .env.example         # Example environment variables
├── .gitignore           # Files ignored by Git
├── .python-version      # Python version used by UV
├── main.py              # Context-aware agent demonstrations
├── pyproject.toml       # Project configuration and dependencies
├── uv.lock              # Locked dependency versions
└── README.md            # Project documentation
```

---

# 🧩 What Is Runtime Context?

Runtime context is application-managed data that is passed to an agent during execution.

In this project, the application creates a `UserContext` object:

```python
@dataclass
class UserContext:
    username: str
    user_id: int
    city: str
    email: str | None = None
    search_count: int = 0
```

The context object is passed to the agent through:

```python
result = await Runner.run(
    starting_agent=agent,
    input="Find a mathematics tutor near me.",
    context=user_context,
)
```

The `context=user_context` argument makes the context available to:

* Dynamic agent instructions
* Function tools
* Application-controlled agent logic

The context is not automatically added to the LLM prompt.

---

## 🔄 Runtime Context Flow

```text
Python Application
        │
        │ Creates UserContext
        ▼
UserContext Object
        │
        │ Passed through Runner.run()
        ▼
OpenAI Agents SDK
        │
        ├──► Dynamic Instructions
        │
        ├──► Function Tools
        │
        └──► Application Logic
```

The developer controls which context values are exposed to the LLM.

---

# 👤 `UserContext`

The project uses a Python dataclass to define the structure of the runtime context.

```python
@dataclass
class UserContext:
    username: str
    user_id: int
    city: str
    email: str | None = None
    search_count: int = 0
```

### Context fields

| Field          | Type          | Required | Purpose                                    |
| -------------- | ------------- | -------: | ------------------------------------------ |
| `username`     | `str`         |      Yes | Used for personalized agent instructions   |
| `user_id`      | `int`         |      Yes | Internal application identifier            |
| `city`         | `str`         |      Yes | Used by context-aware search tools         |
| `email`        | `str \| None` |       No | Optional user information                  |
| `search_count` | `int`         |       No | Tracks searches during the current runtime |

Required fields do not have default values:

```python
username: str
user_id: int
city: str
```

Optional fields have default values:

```python
email: str | None = None
search_count: int = 0
```

---

# 🔐 Context Is Not Automatically Visible to the LLM

A common misunderstanding is:

> If data exists inside `UserContext`, the LLM automatically receives it.

That is not how this project works.

For example:

```python
user_context = UserContext(
    username="Abdullah",
    user_id=101,
    city="Karachi",
    email="abdullah@example.com",
)
```

The context object contains several values, but the LLM does not automatically receive all of them.

The application decides whether a value should be exposed.

```text
UserContext
├── username
├── user_id
├── city
├── email
└── search_count
        │
        │ Developer controls access
        ▼
Agent Instructions / Tools
        │
        │ Only selected values are returned
        ▼
LLM
```

---

# 🤖 Demo 1: Dynamic Agent Instructions

The first agent uses runtime context to generate personalized instructions.

```python
async def build_math_instructions(
    context: RunContextWrapper[UserContext],
    agent: Agent[UserContext],
) -> str:
    user = context.context

    return (
        f"You are {agent.name}, a helpful mathematics assistant. "
        f"The current user's name is {user.username}. "
        "Use the user's name naturally when appropriate."
    )
```

The function receives:

```python
context: RunContextWrapper[UserContext]
```

The original context object is accessed through:

```python
user = context.context
```

The username is included in the returned instruction string:

```python
f"The current user's name is {user.username}."
```

Therefore, the username becomes visible to the LLM.

### Data flow

```text
UserContext.username
        │
        ▼
build_math_instructions()
        │
        ▼
Returned instruction string
        │
        ▼
LLM
```

This is intentional because the agent needs the username to personalize its response.

---

# 🔒 Demo 2: Context-Aware Tool With Controlled Data Exposure

The profile tool accesses the internal `user_id`:

```python
@function_tool
async def check_profile(
    context: RunContextWrapper[UserContext],
) -> str:
    user = context.context

    print(
        f"[INTERNAL] Checking profile "
        f"for user ID: {user.user_id}"
    )

    return "The user profile is active."
```

The Python tool can access:

```python
user.user_id
```

However, the tool returns only:

```text
The user profile is active.
```

The raw `user_id` is not included in the returned tool result.

### Data flow

```text
UserContext.user_id
        │
        ▼
Python Function Tool
        │
        ▼
Internal Application Logic
        │
        ▼
Safe Tool Result
        │
        ▼
LLM
```

The LLM receives the tool result, not every internal value accessed by the tool.

---

# 🔎 Demo 3: Context-Aware Asynchronous Tool

The tutor search tool uses the user's city:

```python
@function_tool
async def search_math_tutor(
    context: RunContextWrapper[UserContext],
    query: str,
) -> str:
    user = context.context

    print(f"[INTERNAL] Search city: {user.city}")

    await asyncio.sleep(1)

    return (
        f"No mathematics tutors were found "
        f"for '{query}'."
    )
```

The tool receives two sources of information:

```python
context
```

Provides application-managed information:

```python
user.city
```

```python
query
```

Provides the search request generated from the user's message.

### Data flow

```text
User Message
      │
      ▼
LLM creates tool arguments
      │
      ▼
query
      │
      ├──────────────┐
      │              │
      ▼              ▼
Function Tool ◄── UserContext.city
      │
      ▼
Tool Result
      │
      ▼
LLM
```

The application can use user-specific context without requiring the user to provide the city in every message.

---

# ⚡ Why `asyncio.sleep()` Is Used

The tools are asynchronous:

```python
async def search_math_tutor(...):
```

Therefore, the code uses:

```python
await asyncio.sleep(1)
```

Instead of:

```python
time.sleep(1)
```

`asyncio.sleep()` allows the event loop to continue handling other asynchronous work while the current task is waiting.

`time.sleep()` blocks the event loop and should generally be avoided inside asynchronous functions.

---

# 🔢 Demo 4: Mutable Runtime State

The `search_count` field tracks how many times the learning-resource tool has been used.

```python
user.search_count += 1
```

The same `UserContext` object is reused:

```python
first_search = await Runner.run(
    starting_agent=stateful_search_agent,
    input="Search for Python learning resources.",
    context=user_context,
)

second_search = await Runner.run(
    starting_agent=stateful_search_agent,
    input="Search for Agentic AI learning resources.",
    context=user_context,
)
```

Because the same context object is passed to both runs, changes to `search_count` remain available during the current application runtime.

### State flow

```text
Initial State

search_count = 0
        │
        ▼
First Tool Call

search_count = 1
        │
        ▼
Second Tool Call

search_count = 2
        │
        ▼
Third Tool Call

search_count = 3
```

This demonstrates mutable runtime state.

---

# 🧠 Runtime Context Is Not Persistent Memory

The following value:

```python
search_count
```

remains available only while the current Python application is running and the same context object is reused.

If the application stops:

```text
Application stops
        │
        ▼
UserContext object is removed from memory
        │
        ▼
Runtime state is lost
```

Therefore:

```text
Runtime Context ≠ Persistent Memory
```

For persistent memory, an application would need external storage such as:

* PostgreSQL
* MongoDB
* Redis
* SQLite
* A vector database
* A dedicated memory system

---

# 🆚 Runtime Context vs Conversation History

| Feature                      | Runtime Context           | Conversation History           |
| ---------------------------- | ------------------------- | ------------------------------ |
| Created by                   | Application               | User and assistant interaction |
| Contains                     | Application-managed data  | Previous messages              |
| Passed through               | `context=`                | `input=`                       |
| Automatically visible to LLM | No                        | Yes, when included in input    |
| Can contain internal values  | Yes                       | Usually not recommended        |
| Purpose                      | Runtime application state | Conversation continuity        |

Example runtime context:

```python
UserContext(
    username="Abdullah",
    user_id=101,
    city="Karachi",
)
```

Example conversation history:

```python
[
    {
        "role": "user",
        "content": "What is Agentic AI?"
    },
    {
        "role": "assistant",
        "content": "Agentic AI refers to..."
    },
]
```

These are different concepts and serve different purposes.

---

# 🆚 Runtime Context vs Global Variables

A global variable might look like this:

```python
current_user = {
    "username": "Abdullah",
    "user_id": 101,
}
```

Although global variables can work in a simple script, they are not a suitable design for multi-user applications.

Runtime context is preferable because it is explicitly passed to a specific agent run:

```python
await Runner.run(
    starting_agent=agent,
    input=user_message,
    context=user_context,
)
```

This makes the data flow explicit and easier to manage.

---

# 🚀 Installation

## 1. Clone the repository

```bash
git clone https://github.com/Haris-Shahid/agentic-ai-playground.git
```

Move into the project directory:

```bash
cd agentic-ai-playground/04-tools/02-context-aware-agents
```

---

## 2. Install Python 3.12

```bash
uv python install 3.12
```

---

## 3. Create the environment

```bash
uv sync
```

If the virtual environment does not exist, UV will create it automatically.

---

## 4. Configure environment variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key
BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
```

Do not commit the `.env` file to Git.

---

## 5. Run the application

```bash
uv run main.py
```

---

# 📦 Dependencies

Install dependencies using UV:

```bash
uv add openai-agents
uv add python-dotenv
```

Then run:

```bash
uv sync
```

---

# 📚 Learning Outcomes

After completing this project, I learned how to:

* Create typed runtime context using a dataclass
* Pass context through `Runner.run()`
* Use `RunContextWrapper`
* Access context inside dynamic instructions
* Access context inside function tools
* Control which context values are exposed to the LLM
* Keep selected application values inside Python logic
* Create asynchronous function tools
* Use `asyncio.sleep()` in asynchronous code
* Update mutable state inside runtime context
* Reuse the same context object across multiple agent runs
* Distinguish runtime context from conversation history
* Distinguish runtime context from persistent memory
* Avoid using global variables for user-specific runtime data

---

# 📚 Learning Resources

## OpenAI Agents SDK

https://openai.github.io/openai-agents-python/

## Context Guide

https://openai.github.io/openai-agents-python/context/

## Function Tools

https://openai.github.io/openai-agents-python/tools/

## Agents

https://openai.github.io/openai-agents-python/agents/

## Running Agents

https://openai.github.io/openai-agents-python/running_agents/

## Google Gemini OpenAI Compatibility

https://ai.google.dev/gemini-api/docs/openai

## UV Documentation

https://docs.astral.sh/uv/

## Python Dataclasses

https://docs.python.org/3/library/dataclasses.html

## Python Asyncio

https://docs.python.org/3/library/asyncio.html

---

# ⚠️ Important Notes

* Runtime context is application-managed data.
* Context is not automatically included in the LLM prompt.
* The developer controls which values are exposed.
* A tool can access internal context values without returning them to the LLM.
* Returning a value from a tool makes that result available to the agent workflow.
* Runtime context is not persistent memory.
* Runtime state is lost when the application stops unless it is stored externally.
* Reusing the same context object allows mutable state to remain available during the current runtime.

---

# 📄 License

MIT
