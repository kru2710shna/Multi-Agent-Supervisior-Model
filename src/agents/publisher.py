from __future__ import annotations
from pathlib import Path
from typing import Literal
from langgraph.types import Command
from src.state_schema import State

# Where to save published posts
OUTPUTS_DIR = Path(__file__).resolve().parents[2] / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

def publisher_agent(state: State) -> Command[Literal["Supervisor", "__end__"]]:
    """
    Saves the final blog post content to a markdown file.

    - Looks at the accumulated messages
    - Finds the writer agent's main output (blog post)
    - Filters out system / transition messages
    - Writes the blog post to a markdown file
    """

    print("📤 Publisher Agent: Starting content publication...")

    messages = state["messages"]
    final_content = "⚠️ No content generated."

    # Iterate backward to find last non-system assistant message
    for msg in reversed(messages):
        role = msg.get("role") if isinstance(msg, dict) else getattr(msg, "role", None)
        content = msg.get("content") if isinstance(msg, dict) else getattr(msg, "content", "")

        if role == "system":
            continue

        if not str(content).strip():
            continue

        if any(
            phrase in str(content)
            for phrase in [
                "Transitioning to",
                "Supervisor decided to call",
                "Completed",
                "Next step",
                "Research completed",
                "Writing completed",
            ]
        ):
            continue

        final_content = str(content)
        break

    # Save to markdown file
    output_file = OUTPUTS_DIR / "final_blog_post.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(final_content)

    print(f"✅ Publisher Agent: Blog post saved to {output_file}")

    return Command(
        goto="__end__",
        update={
            "messages": state["messages"]
            + [
                {"role": "system", "content": "Publication completed."},
                {"role": "assistant", "content": final_content},
            ]
        },
    )
