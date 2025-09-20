from __future__ import annotations

from typing import Annotated , Literal 

from utils.model import get_chat_model
from langgraph.graph import MessageState
from langgraph.types import Command
from travily import TavilyClient
from utils.config import settings

_travily = None
try:
    if settings.travily_api_key:
        _travily = TavilyClient(api_key = settings.travily_api_key)
except Exception:
    _travily= None


@tool
def web_search(query:str)-> str:
    """
    Searches the web for current information on a topic 
    """ 
    
    if _travily is None:
        return "Travily not configured. Please set travily_api_key: to enable web search"
    
    data = _travily.search(query=query, search_dept='basic', max_results =2)
    return str(data)

def research_agent(state:MessageState) -> Command[Literal['Supervisior']]:
    """
    Coduct research and gathers information for the blog post
    
    Uses web search to find revelant facts, satistics and sources to support
    the content plan and provide accurate infromation for the blog post
    """
    
    print("Research Agent: Starting Research")
    
    model = get_chat_model()
    
    system = {
        "You are the research specilist. Use the web search tool to gather revelant facts and statistics"
        "and sources for the blog post. Focus on finding credible, current infromation that supports the content plan"
    }
    
    messages = state["message"] + [{"role":"system", "content":system}]
    
    research_query = f"research {state['message'][-1].content if state['message']else 'blog post topic'}"
    
    observe = web_search.invoke()
    
    research_prompt = f"Based on the web search results, create a research summary with key facts , statistics and sources for the blog post: ]\n\n{observe}"
    research_summary = model.invoke([{"role": "user", "content": research_prompt}])
    
    print("Research Agent: Research Completed")
    
    return Command(
        goto= "Supervisior",
        update= {
            "message": [research_summary, {"role": "user", "content": "Research Completed. Ready for Writing phase"}]
        }
    )