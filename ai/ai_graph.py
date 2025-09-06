from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages

from ai.prompts.summarize import summarizer_prompt

load_dotenv()


# ----------------------------
# Graph state
# ----------------------------
class State(TypedDict):
    messages: Annotated[list, add_messages]  # keeps rolling history


# ----------------------------
# LLM setup
# ----------------------------

# Build a dict mapping all categories to BLOCK_NONE

safety_dict = {cat: HarmBlockThreshold.BLOCK_NONE for cat in HarmCategory}

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    safety_settings=safety_dict,
    max_tokens=None,
    timeout=None,
)

# ----------------------------
# Graph builder
# ----------------------------
graph_builder = StateGraph(State)


def summarizer(state: State):
    # Original conversation history
    messages = state["messages"]

    # Prepend the system message so TLDR knows its role
    full_messages = [{"role": "system", "content": summarizer_prompt()}] + messages

    # Get LLM response
    response = llm.invoke(full_messages)

    # Keep only the last assistant message
    return {"messages": [response]}


graph_builder.add_node("summarizer", summarizer)
graph_builder.add_edge(START, "summarizer")
graph_builder.add_edge("summarizer", END)

graph = graph_builder.compile()


# ----------------------------
# Public function to use graph
# ----------------------------
def summarize_text(user_text: str) -> str:
    """Takes plain text and returns the LLM summary."""
    state = graph.invoke({"messages": [{"role": "user", "content": user_text}]})
    last_response = state["messages"][-1]
    print(last_response.content)
    return last_response.content
