# Multi-Agent Supervisor Model

## 📌 Overview
This project demonstrates a **multi-agent workflow** for content creation using LangGraph.  
It orchestrates 4 agents:
- **Content Planner** → generates outline, audience, and structure
- **Research Agent** → gathers supporting info and citations
- **Writer Agent** → produces a polished blog post
- **Publisher Agent** → saves final content to Markdown

## ⚙️ Tech Stack
- Python 3.10+
- LangGraph
- LangChain
- OpenAI / other LLMs
- Tavily API (for research)
- FastMCP (optional)

## 🚀 Usage
```bash
# clone repo
git clone https://github.com/kru2710shna/Multi-Agent-Supervisior-Model.git
cd Multi-Agent-Supervisior-Model

# create environment
python -m venv .venv
source .venv/bin/activate

# install deps
pip install -r requirements.txt
