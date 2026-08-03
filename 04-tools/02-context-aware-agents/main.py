import asyncio
import os
from dataclasses import dataclass

from dotenv import load_dotenv, find_dotenv
from agents import (
    Agent,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    RunContextWrapper,
    Runner,
    function_tool,
    set_tracing_disabled,
)

# Find the nearest .env file and load its values into the environment.
load_dotenv(find_dotenv())

gemini_api_key: str | None = os.getenv("GEMINI_API_KEY") 
base_url: str | None = os.getenv("BASE_URL")

# Validate the required Gemini API key before creating the API client.
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. \nAdd it to your .env file.")

# Validate the required API base URL.
if not base_url:
    raise ValueError("BASE_URL is not set. \nAdd it to your .env file.")


# Disable OpenAI Agents SDK tracing for a cleaner beginner demo. 
# Tracing can be enabled later for debugging, observability, and monitoring.
set_tracing_disabled(disabled=True)

# Create an asynchronous OpenAI-compatible client. 
# 
# Required values: 
# - api_key: Authenticates requests with the Gemini API. 
# - base_url: Points the OpenAI client to Gemini's compatible API endpoint.
external_client: AsyncOpenAI = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url=base_url
)

# Configure the Gemini model through the OpenAI-compatible model adapter. 
# 
# Required values: 
# - model: The model identifier provided by the LLM service. 
# - openai_client: The configured API client used to send requests.
llm_model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gemini-3.6-flash",
    openai_client=external_client
)

@dataclass
class UserContext:
    """Store runtime data for the current user."""

    username: str 
    user_id: int 
    city: str 
    email: str | None = None 
    search_count: int = 0


# The OpenAI Agents SDK calls this function before running the agent.
def build_math_instructions(
        context: RunContextWrapper[UserContext],
        agent: Agent[UserContext]
) -> str:
    """Generate personalized instructions using runtime context."""

    user: UserContext = context.context

    # Important: 
    # The username is intentionally included in the returned string. 
    # Therefore, the username becomes visible to the LLM.
    return(
        f"You are {agent.name}, a helpful mathematics assistant. "
        f"The current user's name is {user.username}. " 
        "Use the user's name naturally when appropriate. " 
        "Explain answers clearly and briefly."
    )

# The tool can access internal application data through context.
@function_tool
async def check_profile(
    context: RunContextWrapper[UserContext]
) -> str:
    """Check the current user's profile status."""

    user: UserContext = context.context

    # This is an internal application operation. 
    # The raw user_id is available to Python code but is not returned 
    # to the LLM.
    print( 
        f"[INTERNAL] Checking profile " 
        f"for user ID: {user.user_id}" 
    )

    await asyncio.sleep(1)

    # Privacy behavior: 
    # The tool reads the internal user_id but does not include it in the returned result. 
    # Therefore, the raw user_id is not passed to the LLM through this tool output.
    # Only this safe result is returned to the agent workflow.
    return "The user profile is active."


# The tool reads the user's city internally. 
# The city is not automatically visible to the LLM unless it is included in the returned string.
@function_tool
async def search_math_tutor( 
    context: RunContextWrapper[UserContext], 
    query: str, 
) -> str: 
    """Search for a mathematics tutor using the user's city."""

    user: UserContext = context.context 


    # Log internal information for demonstration purposes.
    print(f"[INTERNAL] Search city: {user.city}") 
    print(f"[INTERNAL] Search query: {query}")

    await asyncio.sleep(1) 

    # Return only the intended result to the agent.
    return ( 
        f"No mathematics tutors were found " 
        f"for '{query}'." 
    )

# The search_count value is updated on the same UserContext object. 
# If the same context object is reused in multiple Runner.run() calls, 
# the updated value remains available during the lifetime of the Python application. 
# This is runtime state, not persistent memory.
@function_tool 
async def search_learning_resource( 
    context: RunContextWrapper[UserContext], 
    query: str, 
) -> str: 
    """Search for a learning resource and update runtime state."""

    user: UserContext = context.context 

    # Update mutable runtime state. 
    user.search_count += 1 

    print( 
        f"[INTERNAL] Search count: " 
        f"{user.search_count}" 
    )

    await asyncio.sleep(1) 

    # Return the result that the agent can use.
    return ( 
        f"Learning-resource search completed " 
        f"for '{query}'." 
    )

# Agent 1: 
# Demonstrates context used in dynamic instructions.
personalized_math_agent: Agent[UserContext] = Agent(
    name="Math Assistant",
    instructions=build_math_instructions,
    model=llm_model
)

# Agent 2: 
# Demonstrates private application data accessed by a function tool.
private_profile_agent: Agent[UserContext] = Agent( 
    name="Profile Assistant",
    instructions=( 
        "Help users check their profile status. " 
        "Use the check_profile tool when needed." 
    ),
    model=llm_model,
    tools=[check_profile]
)

# Agent 3: 
# Demonstrates user-specific context inside an asynchronous tool.
tutor_search_agent: Agent[UserContext] = Agent( 
    name="Tutor Search Assistant", 
    instructions=( 
        "Help users search for mathematics tutors. " 
        "Always use the search_math_tutor tool " 
        "for tutor searches." 
    ), 
    model=llm_model,
    tools=[search_math_tutor]
)

# Agent 4: 
# Demonstrates mutable runtime state stored in UserContext.
stateful_search_agent: Agent[UserContext] = Agent( 
    name="Learning Resource Assistant", 
    instructions=( 
        "Help users search for learning resources. " 
        "Always use the search_learning_resource tool." 
    ), 
    model=llm_model, 
    tools=[search_learning_resource] 
)

async def run_demos() -> None: 
    """ 
    Run all context demonstrations. 
    
    A single UserContext object is created and reused across all agent runs. 
    This demonstrates that the same runtime context can be shared with multiple agents. 
    
    """

    user_context: UserContext = UserContext( 
        username="Abdullah", 
        user_id=101, 
        city="Karachi", 
        email="abdullah@example.com" 
    )

    # ------------------------------------------------------------------------ 
    # DEMO 1: PERSONALIZED DYNAMIC INSTRUCTIONS 
    # ------------------------------------------------------------------------

    print("\n" + "=" * 70) 
    print("DEMO 1: PERSONALIZED MATH AGENT") 
    print("=" * 70)

    math_result = await Runner.run( 
        starting_agent=personalized_math_agent, 
        input="What is 25 multiplied by 4?", 
        context=user_context 
    )

    print(math_result.final_output) 


    # ------------------------------------------------------------------------ 
    # DEMO 2: PRIVATE PROFILE CONTEXT 
    # ------------------------------------------------------------------------

    print("\n" + "=" * 70) 
    print("DEMO 2: PRIVATE PROFILE AGENT") 
    print("=" * 70)

    profile_result = await Runner.run( 
        starting_agent=private_profile_agent, 
        input="Is my profile active?", 
        context=user_context 
    )

    print(profile_result.final_output) 

    # ------------------------------------------------------------------------ 
    # DEMO 3: CONTEXT-AWARE ASYNCHRONOUS SEARCH 
    # ------------------------------------------------------------------------

    print("\n" + "=" * 70) 
    print("DEMO 3: CONTEXT-AWARE TUTOR SEARCH") 
    print("=" * 70)


    tutor_result = await Runner.run( 
        starting_agent=tutor_search_agent, 
        input="Find a mathematics tutor near me.", 
        context=user_context 
    
    )

    print(tutor_result.final_output) 

    # ------------------------------------------------------------------------ 
    # DEMO 4: MUTABLE RUNTIME STATE 
    # ------------------------------------------------------------------------

    print("\n" + "=" * 70) 
    print("DEMO 4: MUTABLE RUNTIME STATE") 
    print("=" * 70)

    # Reuse the same user_context object for every run. 
    # 
    # The search_count value is updated by the function tool and remains 
    # available because the same context object is reused. 
    
    first_search = await Runner.run( 
        starting_agent=stateful_search_agent, 
        input="Search for Python learning resources.", 
        context=user_context 
    ) 

    print(first_search.final_output)

    second_search = await Runner.run( 
        starting_agent=stateful_search_agent, 
        input="Search for Agentic AI learning resources.", 
        context=user_context
    ) 

    print(second_search.final_output) 

    third_search = await Runner.run( 
        starting_agent=stateful_search_agent, 
        input="Search for OpenAI Agents SDK tutorials.", 
        context=user_context 
    ) 

    print(third_search.final_output) 

    # Display the final runtime state.
    
    print("\n" + "-" * 70)
    print( 
        f"\nFinal runtime search count: " 
        f"{user_context.search_count}" 
    )
    print("-" * 70)

    print( 
        "\nNote: This value exists only while the application is running. " 
        "It is not persistent memory." 
    )



if __name__ == "__main__":
    asyncio.run(run_demos())
