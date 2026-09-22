# AI Research Agent

A simple AI research agent built using **Groq, LangChain, LangGraph, and LangSmith**.

The agent can search the web, read webpages, collect information, and generate a final research answer.

## Technologies Used

* **Groq** – runs the LLM
* **LangChain** – connects the LLM with tools
* **LangGraph** – controls the agent workflow
* **LangSmith** – tracing and debugging
* **DuckDuckGo Search** – free web search
* **BeautifulSoup** – extracts text from webpages

## How It Works

```text
User Question
     ↓
Groq LLM
     ↓
Need research?
     ↓
Web Search
     ↓
Read Webpages
     ↓
Analyze Information
     ↓
Final Answer
```

## Installation

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_key

LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_langsmith_key
LANGSMITH_PROJECT=AI-Research-Agent
```

## Run

```bash
python main.py
```

Example question:

```text
Research RAG in AI and explain how it works.
```

## Project Structure

```text
AI-Research-Agent/
├── main.py
├── agent.py
├── tools.py
├── requirements.txt
├── .gitignore
└── README.md
```
