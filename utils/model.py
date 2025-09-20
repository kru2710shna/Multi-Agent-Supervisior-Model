from __future__ import annotations
import os
from langchain_openai import ChatOpenAI

def get_chat_model() -> ChatOpenAI:
    model_name = os.getenv("OEPNAI_API", "")
    return ChatOpenAI(model=model_name, temprature= 0)


    
    