import os
import uuid
from dotenv import load_dotenv
from supervisior_graph import build_graph
from langchain_core.messages import BaseMessage


# Load environment variables
load_dotenv()

def create_content(prompt: str) -> dict:
    """Run the Supervisor workflow to create content."""
    graph = build_graph()

    # Create a unique session id
    session_id = str(uuid.uuid4())[:8]

    # Initial state for workflow
    initial_state = {
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "current_stage": "",
        "completed_stages": [],
        "session_id": session_id,
    }

    print(f"🚀 Starting Supervisor Workflow (Session: {session_id})")
    print("=" * 60)

    # Run the workflow
    result = graph.invoke(initial_state)

    print("\n✅ Workflow completed!")
    print(f"📌 Session: {session_id}")
    print(f"📩 Total messages processed: {len(result.get('messages', []))}")
    print(f"📊 Stages completed: {result.get('completed_stages', [])}")
    print("=" * 60)

    return result


if __name__ == "__main__":
    # Example run
    user_prompt = "Write a blog post about the future of AI in education."
    output = create_content(user_prompt)

    # Print final output
    print("\n📝 Final Draft:\n")
    for msg in output.get("messages", []):
        if isinstance(msg, BaseMessage):
            if msg.type == "ai":  # Assistant response
                print(msg.content)
        elif isinstance(msg, dict):  # fallback for dict messages
            if msg.get("role") == "assistant":
                print(msg.get("content"))
