from agents import (
    Agent, 
    AsyncOpenAI, 
    OpenAIChatCompletionsModel, 
    Runner, 
    function_tool,
    set_tracing_disabled
)

import os
from dotenv import load_dotenv, find_dotenv

# Loading the environment variables
load_dotenv(find_dotenv())

# 🚫 Disable tracing for clean output (optional for beginners)
set_tracing_disabled(disabled=True)

# Which LLM Provider to use? -> Google Chat Completions API Service
client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Which LLM Model to use?
model = OpenAIChatCompletionsModel(
    model="gemini-3.6-flash",
    openai_client=client
)

# 🛠️ 3) Define tools (functions wrapped for tool calling)
@function_tool
def multiply(a: int, b: int) -> int:
    """🧮 Exact multiplication (use this instead of guessing math)."""
    print(a, b, a * b, "multiply")
    return a * b

@function_tool
def add_numbers(a: int, b: int) -> int:
    """➕ Exact addition (use this instead of guessing math)."""
    print(a, b, a + b, "addition")
    return a + b


agent = Agent(
    name="Assistant", 
    model=model,
    instructions=("""
            You are a helpful assistant. Always use tools for math questions. Always follow DMAS rule (division, multiplication, addition, subtraction). Explain answers clearly and briefly for beginners.
    """),
    tools=[add_numbers, multiply]
)

prompt = "what is 19 + 23 * 2?"
result = Runner.run_sync(agent, prompt)

print("Agent Response: ", result.final_output)