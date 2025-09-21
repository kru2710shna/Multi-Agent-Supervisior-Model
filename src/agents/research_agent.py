from __future__ import annotations
from langchain.tools import tool
from typing import Literal

from utils.model import get_chat_model
from langgraph.types import Command
from tavily import TavilyClient
from utils.config import settings
from src.state_schema import State


_travily = None
try:
    if settings.travily_api_key:
        _travily = TavilyClient(api_key=settings.travily_api_key)
except Exception:
    _travily = None


@tool
def web_search(query: str) -> str:
    """
    Searches the web for current information on a topic.
    """
    if _travily is None:
        return (
            "Travily not configured. Please set travily_api_key to enable web search."
        )

    data = _travily.search(query=query, search_dept="basic", max_results=2)
    return str(data)


def research_agent(state: State) -> Command[Literal["Supervisor"]]:
    """
    Conducts research and gathers information for the blog post.

    Uses web search to find relevant facts, statistics, and sources to support
    the content plan and provide accurate information for the blog post.
    """

    print("🔎 Research Agent: Starting research...")

    model = get_chat_model()

    system_msg = (
        "You are the research specialist. Use the web search tool to gather relevant "
        "facts and statistics and sources for the blog post. Focus on finding credible, "
        "current information that supports the content plan."
    )

    messages = state["messages"] + [{"role": "system", "content": system_msg}]

    last_msg = state["messages"][-1] if state["messages"] else None


    if last_msg is None:
        research_query = "blog post topic"
    elif hasattr(last_msg, "content"):
        research_query = f"research {last_msg.content}"
    elif isinstance(last_msg, dict):
        research_query = f"research {last_msg.get('content', '')}"
    else:
        research_query = "blog post topic"

    observe = web_search.invoke(research_query)

    research_prompt = (
        f"Based on the web search results, create a research summary with key facts, "
        f"statistics, and sources for the blog post:\n\n{observe}"
    )

    response = model.invoke([{"role": "user", "content": research_prompt}])

    # Normalize response
    if hasattr(response, "content"):
        research_summary = {"role": "assistant", "content": response.content}
    elif isinstance(response, dict):
        research_summary = {
            "role": response.get("role", "assistant"),
            "content": response.get("content", str(response)),
        }
    else:
        research_summary = {"role": "assistant", "content": str(response)}

    print("✅ Research Agent: Research completed.")

    return Command(
    goto="Supervisor",
    update={
        "messages": [
            research_summary,
            {"role": "user", "content": "Research completed. Ready for writing phase."},
        ]
    },
)
