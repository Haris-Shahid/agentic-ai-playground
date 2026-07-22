from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner
import os
from dotenv import load_dotenv, find_dotenv

# Loading the environment variables
load_dotenv(find_dotenv())

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

agent = Agent(name="Assistant", model=model)

result = Runner.run_sync(agent, "Welcome and motivate me to learn Agentic AI")

print("Agent Response: ", result.final_output)