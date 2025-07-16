import os, requests, sys
from bs4 import BeautifulSoup
from langchain.agents import Tool, AgentType
from langchain_groq import ChatGroq
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langgraph.prebuilt import create_react_agent  # <-- NEW IMPORT

# 1. ---------- Plain HTTP scraper ----------
def scrape_url(url: str) -> str:
    """Return raw HTML text for a given URL."""
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    text = soup.get_text(separator="\n", strip=True)
    # Save raw text to disk
    with open("baka.txt", "w", encoding="utf-8") as f:
        f.write(text)
    return f"Raw page saved to baka.txt ({len(text)} chars)."

# 2. ---------- LangChain Tool wrapper ----------
scrape_tool = Tool(
    name="WebScraper",
    func=scrape_url,
    description="Scrapes a web page and writes the raw text to baka.txt"
)

# 3. ---------- Groq LLM ----------
llm = ChatGroq(
    model="gemma2-9b-it",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)

# 4. ---------- Modern agent ----------
agent = create_react_agent(
    model=llm,
    tools=[scrape_tool],
)

# 5. ---------- Run from CLI ----------
if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "https://docs.smith.langchain.com"
    query = f"Scrape the following URL and save the raw text into baka.txt: {url}"
    result = agent.invoke({"messages": [("user", query)]})
    print(result["messages"][-1].content)