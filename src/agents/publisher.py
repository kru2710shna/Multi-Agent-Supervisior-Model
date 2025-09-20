from __future__ import annotations

from pathlib import Path
from typing import Literal

from langgraph.graph import MessageState
from langgraph.types import Command
from langgraph.grpah import END

# Where to save published posts
OUTPUTS_DIR = Path(__file__).resolve().parents[2] / "outputs"

OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def publisher_agent(state: MessageState) -> Command[Literal["supervisor", "__end__"]]:
    """
    Saves the final blog post content to a markdown file.

    This agent:
    - Looks at the accumulated messages
    - Finds the writer agent's main output (blog post)
    - Filters out system and transition messages
    - Writes the blog post to a markdown file
    """

    print("📤 Publisher Agent: Starting content publication...")

    messages = state["messages"]
    final_content = "⚠️ No content generated."

    # Iterate backward to find last non-system message
    for msg in reversed(messages):
        # Skip system-type messages
        if hasattr(msg, "type") and msg.type == "system":
            continue
        if hasattr(msg, "role") and msg.role == "system":
            continue

        # Skip transition messages
        if any(
            phrase in str(msg.content)
            for phrase in [
                "Transitioning to",
                "Moving to",
                "Completed",
                "Ready for",
                "Content planning",
                "Research completed",
                "Writing completed",
                "Supervisor decided to call",
            ]
        ):
            continue

        # Skip empty content
        if not str(msg.content).strip():
            continue

        # Skip research plans / outlines
        if any(
            phrase in str(msg.content)
            for phrase in [
                "What I’ll do next",
                "Key data points I plan to include",
                "Preliminary findings",
                "How I’ll structure the draft",
                "What I need from you",
                "Next step",
            ]
        ):
            continue

        # First good match = our final content
        final_content = str(msg.content)
        break

    # Save to markdown file
    output_file = OUTPUTS_DIR / "final_blog_post.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(final_content)

    print(f"✅ Publisher Agent: Blog post saved to {output_file}")

    return Command(
        goto="__end__",  
        update= [{"messages": [{"role": "system", "content": "Publication completed."}]},
                 {"role": "user", "content": final_content}]
    )
