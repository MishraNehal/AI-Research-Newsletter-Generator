"""
arxiv_tool.py — A proper CrewAI BaseTool for fetching recent AI papers from arxiv.

The original arxiv_tool.py was a plain function that was never connected to any agent.
This version is a proper CrewAI tool that agents can actually call.
"""

from typing import Type
import requests
import xml.etree.ElementTree as ET

from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class ArxivSearchInput(BaseModel):
    """Input schema for ArxivSearchTool."""
    query: str = Field(..., description="Search query, e.g. 'large language models' or 'multimodal AI'")
    max_results: int = Field(default=5, description="Number of papers to return (max 10)")


class ArxivSearchTool(BaseTool):
    name: str = "arxiv_search"
    description: str = (
        "Search arxiv for recent AI/ML research papers. "
        "Returns paper titles, authors, abstracts, and links. "
        "Use this to find specific papers or explore a research topic."
    )
    args_schema: Type[BaseModel] = ArxivSearchInput

    def _run(self, query: str, max_results: int = 5) -> str:
        """Fetch papers from arxiv API and return formatted results."""
        try:
            url = (
                f"http://export.arxiv.org/api/query"
                f"?search_query=all:{query.replace(' ', '+')}"
                f"&start=0&max_results={min(max_results, 10)}"
                f"&sortBy=submittedDate&sortOrder=descending"
            )

            response = requests.get(url, timeout=15)

            if response.status_code != 200:
                return f"Failed to fetch from arxiv (status {response.status_code})"

            # Parse the Atom XML response
            root = ET.fromstring(response.text)
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            entries = root.findall('atom:entry', ns)

            if not entries:
                return f"No papers found on arxiv for query: '{query}'"

            results = []
            for i, entry in enumerate(entries, 1):
                title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
                authors = [a.find('atom:name', ns).text for a in entry.findall('atom:author', ns)]
                author_str = ', '.join(authors[:3])
                if len(authors) > 3:
                    author_str += f" et al."
                link = entry.find('atom:id', ns).text.strip()
                summary = entry.find('atom:summary', ns).text.strip()[:300].replace('\n', ' ')

                results.append(
                    f"{i}. **{title}**\n"
                    f"   Authors: {author_str}\n"
                    f"   Link: {link}\n"
                    f"   Abstract (excerpt): {summary}...\n"
                )

            return "\n".join(results)

        except requests.exceptions.Timeout:
            return "arxiv request timed out. Try a simpler query."
        except Exception as e:
            return f"Error fetching from arxiv: {str(e)}"


# ✅ Instantiate once — import this in crew.py
arxiv_tool = ArxivSearchTool()