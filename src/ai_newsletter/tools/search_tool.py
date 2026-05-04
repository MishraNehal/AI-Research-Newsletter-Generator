"""
search_tool.py — Enhanced Serper search tool for the AI Newsletter crew.

Improvements over the default SerperDevTool():
- n_results=10 → gives researcher more signal to pick the best 5 papers
- country="us"  → biases results toward English-language AI research sources
- A second news_search_tool scoped to recent news only (type="news")
  so the researcher can also pick up model releases and blog posts,
  not just academic papers.
"""

from crewai_tools import SerperDevTool

# General web search — used for arxiv, HuggingFace, papers with code, etc.
search_tool = SerperDevTool(
    n_results=10,      # fetch more results so agent can be selective
    country="us",      # English-language sources
)

# News search — catches model releases, blog posts, and announcements
news_search_tool = SerperDevTool(
    n_results=5,
    country="us",
    search_type="news",   # scoped to news tab in Google
)