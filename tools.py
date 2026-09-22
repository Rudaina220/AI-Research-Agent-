import json
import requests

from bs4 import BeautifulSoup
from ddgs import DDGS
from langchain_core.tools import tool


@tool
def web_search(query: str) -> str:
    """
    Search the internet for information.
    Use this tool to find relevant webpages and sources.
    """

    try:
        results = DDGS().text(
            query,
            max_results=5
        )

        formatted_results = []

        for result in results:
            formatted_results.append({
                "title": result.get("title"),
                "url": result.get("href"),
                "snippet": result.get("body")
            })

        return json.dumps(
            formatted_results,
            indent=2,
            ensure_ascii=False
        )

    except Exception as e:
        return f"Search error: {str(e)}"


@tool
def web_readpage(url: str) -> str:
    """
    Read the text content of a webpage URL.
    Use this after web_search when detailed information is needed.
    """

    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 Chrome/120 Safari/537.36"
            )
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        for element in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "aside"
        ]):
            element.decompose()

        text = soup.get_text(
            separator=" ",
            strip=True
        )

        text = " ".join(text.split())

        return text[:12000]

    except Exception as e:
        return f"Webpage reading error: {str(e)}"