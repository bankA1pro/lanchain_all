```markdown
# 🗺️ One-File Journey: LangChain Agent Scraping & Saving to `baka.txt`

**Author:** @bankA1pro  
**Date:** 2025-07-16  
**Goal:** Build a **LangChain Agent** that  
1. Scrapes any URL  
2. Saves raw text to `baka.txt`  
3. Uses **Groq’s LLM** (`gemma2-9b-it`)

---

## 1️⃣ Initial Plan & Requirements

| Item        | Decision                         |
|-------------|----------------------------------|
| Framework   | LangChain (legacy)               |
| LLM         | ChatGroq (`gemma2-9b-it`)        |
| Tool        | Custom `WebScraper`              |
| Output File | `baka.txt` (UTF-8)               |
| Parser      | `lxml` (later switched)          |

---

## 2️⃣ First Code Attempt

```python
# search_agent.py
import os, sys, requests
from bs4 import BeautifulSoup
from langchain.agents import Tool, initialize_agent, AgentType
from langchain_groq import ChatGroq

llm = ChatGroq(model="gemma2-9b-it", groq_api_key=os.getenv("GROQ_API_KEY"))

def scrape_url(url: str) -> str:
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "lxml")   # ← culprit
    text = soup.get_text(separator="\n", strip=True)
    with open("baka.txt", "w", encoding="utf-8") as f:
        f.write(text)
    return f"Saved {len(text)} chars to baka.txt"

scrape_tool = Tool(name="WebScraper", func=scrape_url, description="Scrapes URL and saves raw text to baka.txt")

agent = initialize_agent(
    tools=[scrape_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
    print(agent.run(f"Scrape {url}"))
```

---

## 3️⃣ First Run & Error

```bash
python search_agent.py https://example.com
```
```
bs4.exceptions.FeatureNotFound: Couldn't find a tree builder with the features you requested: lxml.
```

---

## 4️⃣ Fix Missing Parser

| Option | Command |
|--------|---------|
| **A** (install) | `pip install lxml` |
| **B** (switch)  | Use built-in parser: `html.parser` |

Applied **B** (lightweight):

```python
soup = BeautifulSoup(resp.text, "html.parser")
```

---

## 5️⃣ Deprecation Warnings

| Warning | Modern Replacement |
|---------|--------------------|
| `initialize_agent` | `create_react_agent` |
| `agent.run(...)`   | `agent.invoke(...)` |

---

## 6️⃣ Final Working Script (v1.0)

```python
# search_agent.py
import os, sys, requests
from bs4 import BeautifulSoup
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from langchain_core.tools import tool

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
llm = ChatGroq(model="gemma2-9b-it", groq_api_key=GROQ_API_KEY)

@tool
def scrape_url(url: str) -> str:
    """Scrapes a web page and saves raw text to baka.txt."""
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    text = soup.get_text(separator="\n", strip=True)
    with open("baka.txt", "w", encoding="utf-8") as f:
        f.write(text)
    return f"Saved {len(text)} chars to baka.txt"

agent = create_react_agent(model=llm, tools=[scrape_url])

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
    print(agent.invoke({"messages": [("user", f"Scrape {url}")]})["messages"][-1].content)
```

---

## 7️⃣ Verification

```bash
python search_agent.py https://example.com
# → Saved 173 chars to baka.txt
```

Check file:
```bash
cat baka.txt
# Example Domain
# This domain is for use in illustrative examples...
```

---

## 8️⃣ Lessons Learned

1. Always list parser deps (`lxml`, `html5lib`, etc.).  
2. Prefer **LangGraph** for new agents.  
3. Use `invoke` instead of legacy `run`.  
4. Provide clear tool descriptions.

---

Happy scraping & LLM-ing! 🚀
```