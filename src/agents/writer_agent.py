from __future__ import annotations

from typing import Annotated, Literal

from utils.model import get_chat_model
from langgraph.types import Command
from tavily import TavilyClient
from utils.config import settings
from src.state_schema import State

def writer_agent(state: State) -> Command[Literal["Supervisor"]]:
    """
    Writes a complete, publishable blog post with facts, citations, and SEO optimization.
    
    Produces a blog post that includes:
    - Compelling headline and introduction
    - Well-structured content with headings
    - Factual claims supported by citations
    - SEO optimization (keywords, meta description)
    - Engaging conclusion
    """

    print("Writer Agent: Starting to write...")

    model = get_chat_model()

    system = (
        "You are a professional content writer. Write a complete, publishable blog post using "
        "the research brief and plan provided.\n\n"
        "CONTENT REQUIREMENTS:\n"
        "- Compelling headline that includes primary keywords\n"
        "- Introduction that hooks the reader and includes target keywords\n"
        "- Well-structured body with clear headings (H2, H3) and subheadings\n"
        "- Factual claims supported by the research with inline citations\n"
        "- Engaging, conversational tone\n"
        "- 800–1200 words of high-quality content\n"
        "- Conclusion with actionable takeaways\n\n"
        "SEO REQUIREMENTS:\n"
        "- Include primary and secondary keywords naturally\n"
        "- Proper heading structure (H1, H2, H3)\n"
        "- Write a compelling meta description (150–160 characters)\n"
        "- Include internal linking suggestions where relevant\n"
        "- Optimize for readability (short paragraphs, bullet points)\n\n"
        "FACT-CHECKING REQUIREMENTS:\n"
        "- Use credible sources and data\n"
        "- Add inline citations for statistics and facts\n"
        "- Flag uncertain claims or add disclaimers\n"
    )

    # Add system message into state
    messages = state["messages"] + [{"role": "system", "content": system}]

    draft = model.invoke(messages)

    print("Writer Agent: Writing completed")

    return Command(
        goto="Supervisor",
        update={
            "messages": [
                draft,
                {"role": "user", "content": "Writing completed. Ready for review phase."}
            ]
        }
    )
