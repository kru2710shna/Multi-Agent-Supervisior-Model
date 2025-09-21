from __future__ import annotations
from typing import Annotated, Literal, TypedDict
from utils.model import get_chat_model
from langgraph.graph import END, StateGraph
from langgraph.types import Command
from utils.config import settings
from src.agents.content_planner import content_planner
from src.agents.research_agent import research_agent
from src.agents.writer_agent import writer_agent
from src.agents.publisher import publisher_agent
from src.state_schema import State


# ---- Supervisor Node ----
def supervisor_node(state: State) -> Command:
    """LLM-based Supervisor that decides which agent to call next."""

    model = get_chat_model()

    # get current state
    completed = state.get("completed_stages", [])
    current = state.get("current_stage", "")
    session_id = state.get("session_id", "")

    # mark current state as complete
    if current and current not in completed:
        completed.append(current)
        print(f"✅ Completed stage: {current} | Session_id: {session_id}")

    # pipeline stages
    all_stages = ["content_planner", "research_agent", "writer_agent", "publisher"]

    # check if all stages are done
    if len(completed) >= len(all_stages):
        print(f"🎉 All stages completed for session {session_id}")
        return Command(goto="__end__")

    # supervisor LLM prompt
    prompt = f"""
    You are supervising workflow for session {session_id}.
    Based on the current state `{current}`, decide which agent should be called next.

    - CURRENT STATE: {current}
    - SESSION_ID: {session_id}
    - COMPLETED STAGES: {completed}
    - AVAILABLE STAGES: {[s for s in all_stages if s not in completed]}
    
    - WORKFLOW STAGES:
     1. Content Planner: Creates a detailed content plan and outline for the topic
    2. Research Agent: Gathers relevant information and sources for the content
    3. Writer Agent: Creates the actual content based on the plan and research
    4. Publisher: Finalizes and publishes the completed content
    
    
    Choose the next stage from the available stages listed above.
    Respond with ONLY the stage name (e.g., "content_planner").
    Do not include any additional text or explanation.
    """

    messages = state['messages'] + [{"role": "system", "content": prompt}]
    decision = model.invoke(messages).content.strip().lower()

    # fallback to first available stage if LLM is uncertain
    next_stage = next((s for s in all_stages if s not in completed), None)

    if decision in all_stages and decision not in completed:
        next_stage = decision

    print(f"🤖 Supervisor chose next stage: {next_stage}")

    return Command(
        goto=next_stage,
        update={"current_stage": next_stage, "completed_stages": completed},
    )

def build_graph():
    """Builds the multi-agent workflow graph (sequential)."""
    graph = StateGraph(State)

    # add nodes
    graph.add_node("Supervisor", supervisor_node)
    graph.add_node("content_planner", content_planner)
    graph.add_node("research_agent", research_agent)
    graph.add_node("writer_agent", writer_agent)
    graph.add_node("publisher", publisher_agent)

    # ✅ Conditional edges: Supervisor picks *one* agent at a time
    graph.add_conditional_edges(
        "Supervisor",
        lambda state: state["current_stage"],  # Supervisor decides next stage
        {
            "content_planner": "content_planner",
            "research_agent": "research_agent",
            "writer_agent": "writer_agent",
            "publisher": "publisher",
        },
    )

    # agents loop back to Supervisor
    graph.add_edge("content_planner", "Supervisor")
    graph.add_edge("research_agent", "Supervisor")
    graph.add_edge("writer_agent", "Supervisor")

    # ✅ publisher is the final stage → END
    graph.add_edge("publisher", END)

    # entry point
    graph.set_entry_point("Supervisor")

    return graph.compile()