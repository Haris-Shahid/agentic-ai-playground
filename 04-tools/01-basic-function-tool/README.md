# 🛠️ Basic Function Tools with OpenAI Agents SDK

A beginner-friendly Agentic AI project demonstrating how to give an AI agent access to custom Python functions using **Function Tools**.

This project uses the **OpenAI Agents SDK** with **Google Gemini through the OpenAI-compatible API**. The agent can select and call Python tools to perform mathematical operations instead of relying only on the language model to calculate answers.

---

## 📌 Project Overview

Large Language Models can generate answers, but an AI agent can also use external capabilities through tools.

In this project, two Python functions are converted into agent tools:

- `sum()` — performs addition
- `multiply()` — performs multiplication

The agent receives a mathematical question, determines which tool is required, calls the available tool with the appropriate arguments, receives the tool result, and generates the final response.

---

## ✨ Features

- Custom Python function tools
- Multiple tools available to one agent
- Addition tool
- Multiplication tool
- Automatic tool selection by the AI agent
- Automatic tool argument generation
- Google Gemini integration
- OpenAI-compatible API integration
- OpenAI Agents SDK
- Custom agent instructions
- Tool execution logging
- Tracing disabled for cleaner terminal output
- Environment variable management using `python-dotenv`
- UV-based dependency management

---

## 🧰 Tech Stack

- Python 3.12
- UV
- OpenAI Agents SDK
- Google Gemini API
- OpenAI-compatible API
- `python-dotenv`

---

## 📁 Project Structure

```text
01-basic-function-tool/
│
├── .env
├── .env.example
├── .gitignore
├── .python-version
├── main.py
├── pyproject.toml
├── README.md
└── uv.lock
```

---

## 🧠 How Function Tools Work

The application follows this flow:

```text
User Prompt
     ↓
AI Agent analyzes the request
     ↓
Agent checks the available tools
     ↓
Agent selects the required tool
     ↓
Agent generates tool arguments
     ↓
Python tool function executes
     ↓
Tool returns the result
     ↓
Agent generates the final response
```

For the following prompt:

```text
What is 19 + 23 × 2?
```

The agent can process the calculation in this order:

```text
23 × 2 = 46
19 + 46 = 65
```

The expected final answer is:

```text
65
```

---

## 🛠️ Available Tools

### 1. Addition Tool

```python
@function_tool
def add_numbers(a: int, b: int) -> int:
    """Perform exact addition."""
    
    return a + b
```

This tool accepts:

```text
a → first integer
b → second integer
```

It returns:

```text
a + b
```

Example:

```python
add_numbers(19, 46)
```

Result:

```text
65
```

---

### 2. Multiplication Tool

```python
@function_tool
def multiply(a: int, b: int) -> int:
    """Perform exact multiplication."""
    
    return a * b
```

This tool accepts:

```text
a → first integer
b → second integer
```

It returns:

```text
a × b
```

Example:

```python
multiply(23, 2)
```

Result:

```text
46
```

---

## 🔍 Understanding `@function_tool`

```python
@function_tool
def multiply(a: int, b: int) -> int:
```

`@function_tool` is a decorator provided by the OpenAI Agents SDK.

It converts a Python function into a tool that can be provided to an AI agent.

The SDK can use information from:

- Function name
- Function parameters
- Type hints
- Function docstring

For example:

```python
def multiply(a: int, b: int) -> int:
```

provides information such as:

```text
Tool name:
multiply

Parameters:
a
b

Parameter type:
integer

Return type:
integer
```

The docstring describes the purpose of the tool:

```python
"""Exact multiplication."""
```

Clear function names, type hints, and docstrings help the model understand when and how to use a tool.

---

## 🤖 Registering Tools with the Agent

The tools are provided to the agent through the `tools` parameter:

```python
agent = Agent(
    name="Assistant",
    model=model,
    instructions="Always use tools for math questions.",
    tools=[add_numbers, multiply],
)
```

The following line makes both tools available to the agent:

```python
tools=[add_numbers, multiply]
```

Important:

```python
tools=[add_numbers, multiply]
```

is correct because the tool functions are being passed to the agent.

Do not call the tools manually:

```python
tools=[add_numbers(), multiply()]
```

The agent runtime decides when a tool should be called and supplies the required arguments.

---

## 🧮 Tool-Calling Example

Input:

```text
What is 19 + 23 × 2?
```

Possible execution flow:

```text
Agent receives the question
          ↓
Agent identifies multiplication
          ↓
multiply(a=23, b=2)
          ↓
Tool returns 46
          ↓
Agent identifies addition
          ↓
sum(a=19, b=46)
          ↓
Tool returns 65
          ↓
Agent generates the final response
```

The exact internal tool-call sequence may depend on the model and its tool-calling behavior.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Haris-Shahid/agentic-ai-playground.git
```

### 2. Navigate to the project

```bash
cd agentic-ai-playground/04-tools/01-basic-function-tool
```

---

## 🐍 Create a UV Project with Python 3.12

To create a new project directly with Python 3.12:

```bash
uv init --python 3.12 01-basic-function-tool
```

Enter the project directory:

```bash
cd 01-basic-function-tool
```

---

## 📦 Install Dependencies

Add the OpenAI Agents SDK:

```bash
uv add openai-agents
```

Add `python-dotenv`:

```bash
uv add python-dotenv
```

Synchronize the project:

```bash
uv sync
```

---

## 🔐 Configure Environment Variables

Create a `.env` file in the project directory:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Do not add your real API key to GitHub.

The `.env` file should be included in `.gitignore`.

Example:

```gitignore
.env
.venv/
__pycache__/
*.pyc
```

You can commit an `.env.example` file:

```env
GEMINI_API_KEY=your_gemini_api_key
```

---

## ▶️ Run the Project

Run:

```bash
uv run main.py
```

Example output:

```text
23 2 46 multiply
19 46 65 addition

Agent Response: 65
```

The exact output may vary depending on the model response.

---

## 🧾 Understanding the Tool Logs

The following line is included in the multiplication tool:

```python
print(a, b, a * b, "multiply")
```

It prints the tool arguments and calculated result to the terminal.

Example:

```text
23 2 46 multiply
```

This means:

```text
First value: 23
Second value: 2
Result: 46
Tool: multiply
```

The following line is included in the addition tool:

```python
print(a, b, a + b, "addition")
```

Example:

```text
19 46 65 addition
```

This means:

```text
First value: 19
Second value: 46
Result: 65
Tool: addition
```

These print statements are useful for learning and debugging because they show when the Python tools are executed.

---

## 🚫 Tracing

Tracing is disabled in this project:

```python
set_tracing_disabled(disabled=True)
```

This keeps the beginner project output cleaner by disabling tracing.

Tracing can be useful in larger applications for observing agent runs, model calls, tool calls, and execution behavior.

---

## 📚 Learning Outcomes

This project helped me learn:

- What an AI agent tool is
- The difference between a normal Python function and a function tool
- How to use `@function_tool`
- How to create custom tools
- How to define multiple tools
- How to register tools with an agent
- How an agent selects a relevant tool
- How tool arguments are generated
- How Python functions are executed through the agent runtime
- How tool results are returned to the agent
- How type hints describe tool parameters
- How docstrings help describe tool behavior
- How to use custom agent instructions
- How to integrate Gemini using an OpenAI-compatible API
- How to use UV for dependency management
- How to disable tracing during development

---

## ⚠️ Important Notes

### Tool Use Depends on the Model

The agent is given this instruction:

```text
Always use tools for math questions.
```

This guides the model to use the available tools for mathematical operations.

However, tool selection is still part of the model's decision-making process.

---

### Tool Names Should Be Clear

Good:

```python
multiply
```

Less clear:

```python
calculate_value
```

A clear tool name makes its purpose easier to understand.

---

### Type Hints Are Important

```python
def multiply(a: int, b: int) -> int:
```

The type hints communicate that:

```text
a → integer
b → integer
result → integer
```

Type hints help define the expected tool input and output.

---

### Avoid Naming a Function `sum`

Python already provides a built-in function named:

```python
sum()
```

Using:

```python
def sum(a: int, b: int) -> int:
```

overrides the built-in `sum` name within the current module.

For this learning example, the function works, but a more professional name would be:

```python
@function_tool
def add_numbers(a: int, b: int) -> int:
    """Add two integers and return the result."""
    
    return a + b
```

Then register it as:

```python
tools=[add_numbers, multiply]
```

This avoids overriding Python's built-in `sum()` function.

---

## ⚡ Using Tool Output as the Final Response

By default, the OpenAI Agents SDK uses:

```python
tool_use_behavior="run_llm_again"
```

The execution flow is:

```text
User
  ↓
Agent selects a tool
  ↓
Tool executes
  ↓
Tool result is sent back to the LLM
  ↓
LLM generates the final response
```

For example, if a tool returns:

```text
59
```

the LLM may process or format the result before generating the final response.

To use the output of the first tool call directly as the final agent response, configure the agent with:

```python
tool_use_behavior="stop_on_first_tool"
```

Example:

```python
@function_tool
def add_numbers(a: int, b: int) -> int:
    """Add two integers."""

    return 59
```

```python
agent = Agent(
    name="Math Assistant",
    instructions="Always use the available math tool.",
    tools=[add_numbers],
    tool_use_behavior="stop_on_first_tool",
)
```

When the user asks:

```text
What is 2 + 2?
```

the execution flow is:

```text
User
  ↓
Agent selects `add_numbers`
  ↓
Tool is called with:

add_numbers(a=2, b=2)

  ↓
Tool returns:

59

  ↓
Agent execution stops
  ↓
Final output:

59
```

The tool result is used directly as the final output, and the LLM does not run again to interpret, correct, explain, or rewrite the result.

### Important Limitation

`stop_on_first_tool` stops the agent after the first tool call.

For a multi-step calculation such as:

```text
19 + 23 × 2
```

the agent may need to call multiple tools:

```text
multiply(23, 2)
→ 46

add_numbers(19, 46)
→ 65
```

If `stop_on_first_tool` is enabled, the agent may stop after the multiplication tool and return:

```text
46
```

Therefore, this behavior is best used when one tool call is sufficient and the tool output should be treated as the authoritative final result.

---

## 🔗 Learning Resources

### OpenAI Agents SDK

https://openai.github.io/openai-agents-python/

### OpenAI Agents SDK — Tools

https://openai.github.io/openai-agents-python/tools/

### OpenAI Agents SDK — Function Tools

https://openai.github.io/openai-agents-python/tools/

### Google Gemini OpenAI Compatibility

https://ai.google.dev/gemini-api/docs/openai

### UV Documentation

https://docs.astral.sh/uv/

### Python Type Hints

https://docs.python.org/3/library/typing.html

---

## 🚀 Next Steps

The next projects in this learning series will cover:

- Tools with multiple parameters
- Tools with optional parameters
- Multiple tool selection
- Async function tools
- Tool context
- Error handling in tools
- Tools with external APIs
- Chainlit integration
- Streaming with tools
- Hosted tools
- MCP tools
- Agent-as-a-tool

---

## License

MIT