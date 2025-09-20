from __future__ import annotations
from typing import Annotated , Literal 

from utils.model import get_chat_model
from langgraph.graph import MessageState
from langgraph.types import Command

def content_planner(state: MessageState) -> Command[Literal["Supervisor"]]:
    """Create a content stratergy and outline for the blog post
    
    Analyzes the user's request and creats a structured plan including:
    - Target audience and tone 
    - Key topics and SubTopics
    - Research Area to Explore
    - Content structure and Flow
    """
    
    print("Content Planner: Starting content planning")
    
    model = get_chat_model()
    
    system = (
        "You are content startergist. Create a comprehensive content plan and outline for the request blog post"
        "Include: target audience, topic , research and content structure and tone reccomendation"
    )
    
    message = state["message"] + [{"role": "system,", "content": system}]
    
    plan = model.invoke(message)
    print("Content Planner: Planning completed")
    
    return Command(
        
        goto = "Supervisor",
        update= {
            "message" : [plan, {"role": "user,", "content": "Planning completed. Ready to Research Phase"}]
        }
    )