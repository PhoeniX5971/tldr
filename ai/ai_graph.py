from typing import Annotated, TypedDict

from dotenv import load_dotenv
from google.ai.generativelanguage_v1beta.types import Tool as GenAITool
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages

from ai.prompts.summarize import summarizer_prompt
from ai.prompts.search import searcher_prompt

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
    model_kwargs={"tools": [GenAITool(google_search={})]},
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


def searcher(state: State):
    # Original conversation history
    messages = state["messages"]

    # Prepend the system message so TLDR knows its role
    full_messages = [{"role": "system", "content": searcher_prompt()}] + messages

    # Get LLM response
    response = llm.invoke(
        full_messages,
    )

    # Keep only the last assistant message
    return {"messages": [response]}


graph_builder.add_node("summarizer", summarizer)
graph_builder.add_node("searcher", searcher)
graph_builder.add_edge(START, "summarizer")
graph_builder.add_edge(START, "searcher")
graph_builder.add_edge("summarizer", END)
graph_builder.add_edge("searcher", END)

graph = graph_builder.compile()


# ----------------------------
# Public function to use graph
# ----------------------------
def invoke_graph(user_text: str, node: str = "summarizer") -> str:
    """
    Invoke the LLM graph and return the response from a specific node.

    :param user_text: The user input text
    :param node: Either "summarizer" or "searcher"
    :return: LLM response content
    """
    if node not in ("summarizer", "searcher"):
        raise ValueError("node must be 'summarizer' or 'searcher'")

    # Tell the graph to start from the selected node
    state = graph.invoke(
        {"messages": [{"role": "user", "content": user_text}]}, start_node=node
    )
    last_response = state["messages"][-1]
    return last_response.content
