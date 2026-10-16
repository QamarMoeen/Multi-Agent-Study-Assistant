
# Import ADK's Agent class.
from google.adk.agents import Agent


# -------------------------
# TOOL 1: CALCULATOR
# -------------------------
# A tool is an ordinary Python function that an agent can call.
def calculate(a: float, b: float, operation: str) -> dict:
    """Calculate two numbers using add, subtract, multiply, or divide."""

    # Perform the requested operation.
    if operation == "add":
        result = a + b

    elif operation == "subtract":
        result = a - b

    elif operation == "multiply":
        result = a * b

    elif operation == "divide":
        # Prevent division by zero.
        if b == 0:
            return {"error": "Cannot divide by zero."}
        result = a / b

    else:
        return {
            "error": "Unsupported operation. Use add, subtract, multiply, or divide."
        }

    # Return a simple result that the agent can explain to the user.
    return {"result": result}


# -------------------------
# TOOL 2: WORD COUNTER
# -------------------------
def count_words(text: str) -> dict:
    """Count the words and characters in a piece of text."""

    # split() separates the text into words.
    words = text.split()

    return {
        "word_count": len(words),
        "character_count": len(text),
    }


# -------------------------
# SPECIALIST AGENT 1
# -------------------------
math_agent = Agent(
    model="gemini-3.5-flash-lite",
    name="math_agent",
    description="Handles arithmetic and calculation requests.",
    instruction="""
    You are a mathematics assistant.
    Use the calculate tool for arithmetic calculations.
    Explain the result clearly and briefly.
    """,
    tools=[calculate],

    # Prevent the specialist from handling the next turn
    # indefinitely or transferring to another specialist.
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)


# -------------------------
# SPECIALIST AGENT 2
# -------------------------
study_agent = Agent(
    model="gemini-3.5-flash-lite",
    name="study_agent",
    description="Helps with study text and word-count requests.",
    instruction="""
    You are a study assistant.
    Use the count_words tool when the user requests a word or
    character count. For ordinary study questions, answer clearly
    and use simple examples.
    """,
    tools=[count_words],

    # Prevent the specialist from handling the next turn
    # indefinitely or transferring to another specialist.
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)


# -------------------------
# ROOT AGENT
# -------------------------
root_agent = Agent(
    model="gemini-3.5-flash-lite",
    name="study_assistant",
    description="Coordinates a team of specialist study agents.",
    instruction="""
    You are the main assistant for an ML/AI student.

    Decide which specialist is best suited to each request.
    - Delegate arithmetic and calculation requests to math_agent.
    - Delegate word-count requests to study_agent.
    - Answer simple general ML/AI study questions yourself.

    Use the specialists when appropriate. Do not claim that a
    tool was used unless it actually was.
    """,
    sub_agents=[math_agent, study_agent],
)