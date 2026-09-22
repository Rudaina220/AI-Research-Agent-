import os

from dotenv import load_dotenv

from langchain_core.messages import SystemMessage
from langchain_groq import ChatGroq

from langgraph.graph import (
    StateGraph,
    START,
    END,
    MessagesState
)

from langgraph.prebuilt import ToolNode

from tools import web_search, web_readpage


load_dotenv()


SYSTEM_PROMPT = """
You are an AI Research Agent.

Your job is to research questions carefully and provide accurate,
well-organized answers.

You have EXACTLY TWO tools available:

1. web_search
   Use this to search the internet.

2. web_readpage
   Use this to open and read a webpage URL returned by web_search.

IMPORTANT:
- Only call tools using their exact names.
- Never invent another tool name.
- Use web_search to find sources.
- Use web_readpage to inspect important sources.
- Search multiple sources when useful.
- Do not invent facts.
- Prefer reliable sources.
- Include useful source URLs in the final answer.
- Stop researching when enough information has been collected.
"""


tools = [
    web_search,
    web_readpage
]


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)


llm_with_tools = llm.bind_tools(tools)


def researcher(state: MessagesState):

    messages = [
        SystemMessage(content=SYSTEM_PROMPT)
    ] + state["messages"]

    response = llm_with_tools.invoke(messages)

    return {
        "messages": [response]
    }


def should_continue(state: MessagesState):

    last_message = state["messages"][-1]

    if getattr(last_message, "tool_calls", None):
        return "tools"

    return "end"


builder = StateGraph(MessagesState)


builder.add_node(
    "researcher",
    researcher
)

builder.add_node(
    "tools",
    ToolNode(tools)
)


builder.add_edge(
    START,
    "researcher"
)


builder.add_conditional_edges(
    "researcher",
    should_continue,
    {
        "tools": "tools",
        "end": END
    }
)


builder.add_edge(
    "tools",
    "researcher"
)


research_agent = builder.compile()