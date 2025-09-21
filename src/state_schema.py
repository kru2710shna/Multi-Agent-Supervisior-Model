from __future__ import annotations
from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list[dict], add_messages] 
    current_stage: str
    completed_stages: list[str]
    session_id: str
