from __future__ import annotations
import os
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI


def get_chat_model():
    provider = os.getenv("MODEL_PROVIDER", "openai")

    if provider == "groq" and os.getenv("GROQ_API_KEY"):
        return ChatGroq(
            model="llama-3.1-8b-instant",  
            api_key=os.getenv("GROQ_API_KEY"),
            temperature=0
            
        )

    if provider == "openai" and os.getenv("OPENAI_API_KEY"):
        return ChatOpenAI(
            model="gpt-4o-mini",
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0,
            max_retries=3
        )

    raise RuntimeError("❌ No valid model provider found. Set MODEL_PROVIDER=groq or openai in .env")
