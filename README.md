# LangChain Web Scraper with Groq LLM

This project demonstrates a simple LangChain agent that scrapes a web page and saves the raw text to a file (`baka.txt`). It utilizes Groq's LLM (`gemma2-9b-it`) for processing.

## Features

*   Scrapes any URL and extracts raw text.
*   Saves the scraped text to `baka.txt`.
*   Uses Groq's `gemma2-9b-it` LLM for agent processing.
*   Implements a custom LangChain tool for web scraping.
*   Uses the modern `langgraph` library for agent creation.

## Prerequisites

*   Python 3.7+
*   `pip` package manager
*   A Groq API key

## Setup

Follow these steps to set up the project locally:

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd lanchain_all/lanchain_scrapper
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3.  **Install dependencies:**

    ```bash
    pip install beautifulsoup4 requests langchain langchain-groq langgraph
    ```

4.  **Set up environment variables:**

    *   Create a `.env` file in the `lanchain_scrapper` directory.
    *   Add your Groq API key to the `.env` file:

        ```
        GROQ_API_KEY=YOUR_GROQ_API_KEY
        ```

        Replace `YOUR_GROQ_API_KEY` with your actual Groq API key.

5.  **Run the script:**

    ```bash
    python search_agent.py <URL_TO_SCRAPE>
    ```

    Replace `<URL_TO_SCRAPE>` with the URL you want to scrape. If no URL is provided, it defaults to `https://docs.smith.langchain.com`.

    Example:

    ```bash
    python search_agent.py https://www.example.com
    ```

    The scraped content will be saved to `baka.txt` in the same directory.

## Step-by-Step Explanation

A detailed step-by-step explanation of the code and the development process can be found in [lanchain_scrapper/step_by_step.md](lanchain_scrapper/step_by_step.md). This document outlines the initial plan, code attempts, error handling, and the final working script.

## Key Components

*   **`search_agent.py`**: The main script containing the LangChain agent and web scraping logic.
*   **`scrape_url(url: str)`**: Function to scrape a given URL using `requests` and `BeautifulSoup4`.
*   **`Tool`**: LangChain's tool abstraction, wrapping the `scrape_url` function.
*   **`ChatGroq`**: LangChain integration for Groq's LLMs.
*   **`create_react_agent`**: Function from `langgraph` to create a React-style agent.