from dotenv import load_dotenv, find_dotenv
import os
from typing import cast

import chainlit as cl

from agents import (
    Agent,
    OpenAIChatCompletionsModel,
    RunConfig,
    Runner,
    AsyncOpenAI,
)


# Load environment variables from the .env file
load_dotenv(find_dotenv())

gemini_api_key = os.getenv("GEMINI_API_KEY")
base_url = os.getenv("BASE_URL")


# Check if the API key is present
if not gemini_api_key:
    raise ValueError(
        "GEMINI_API_KEY is not set. "
        "Please ensure it is defined in your .env file."
    )


# Check if the base URL is present
if not base_url:
    raise ValueError(
        "BASE_URL is not set. "
        "Please ensure it is defined in your .env file."
    )


@cl.on_chat_start
async def start_chat():
    """Set up the chat session when a user connects."""

    # Create the Google Gemini API client
    external_client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url=base_url,
    )

    # Configure the Gemini model
    openai_model = OpenAIChatCompletionsModel(
        model="gemini-3.6-flash",
        openai_client=external_client,
    )

    # Configure the agent run
    config = RunConfig(
        model=openai_model,
        model_provider=external_client,
        tracing_disabled=True,
    )

    # Initialize an empty chat history
    cl.user_session.set("chat_history", [])

    # Store the configuration in the user session
    cl.user_session.set("config", config)

    # Create the AI agent
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant.",
        model=openai_model,
    )

    # Store the agent in the user session
    cl.user_session.set("agent", agent)

    # Send the welcome message
    await cl.Message(
        content="Welcome to Haris AI Assistant! How may I help you?"
    ).send()


@cl.on_message
async def main(message: cl.Message):
    """Process incoming messages and stream the agent response."""

    # Create an empty message for streaming
    msg = cl.Message(content="")
    await msg.send()

    # Retrieve the agent, configuration, and chat history
    agent: Agent = cast(
        Agent,
        cl.user_session.get("agent"),
    )

    config: RunConfig = cast(
        RunConfig,
        cl.user_session.get("config"),
    )

    history = cl.user_session.get("chat_history") or []

    # Add the user's message to the chat history
    history.append(
        {
            "role": "user",
            "content": message.content,
        }
    )

    try:
        print(
            "\n[CALLING_AGENT_WITH_CONTEXT]\n",
            history,
            "\n",
        )

        # Run the agent with streaming enabled
        result = Runner.run_streamed(
            agent,
            history,
            run_config=config,
        )

        # Store the complete streamed response
        response_content = ""

        # Stream the response token by token
        async for event in result.stream_events():

            if (
                event.type == "raw_response_event"
                and hasattr(event.data, "delta")
            ):
                token = event.data.delta

                # Save the token
                response_content += token

                # Display the token in Chainlit
                await msg.stream_token(token)

        # Add the assistant response to the history
        history.append(
            {
                "role": "assistant",
                "content": response_content,
            }
        )

        # Save the updated history in the user session
        cl.user_session.set(
            "chat_history",
            history,
        )

        # Log the conversation
        print(f"User: {message.content}")
        print(f"Assistant: {response_content}")

    except Exception as e:

        error_message = f"Error: {str(e)}"

        msg.content = error_message
        await msg.update()

        print(error_message)