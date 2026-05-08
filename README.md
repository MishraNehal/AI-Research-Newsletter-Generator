# AI Research Newsletter Generator

A multi-agent AI system that researches, summarizes, and generates a weekly AI research newsletter on any topic — automatically.

**Live Demo → [Try it here](https://ai-research-newsletter-generator-pyd9jzujxzswrbsvdptdrv.streamlit.app)**

---

## What it does

You enter a topic. Three AI agents get to work:

1. **Researcher** — searches the web and arxiv for the latest papers
2. **Summarizer** — writes a clear 3-sentence TLDR for each paper
3. **Editor** — assembles everything into a polished newsletter

Output is a ready-to-publish markdown newsletter saved locally and viewable in the browser.

---

## Tech Stack

- **Agent Framework** — CrewAI
- **LLM** — Google Gemini 2.5 Flash Lite
- **Web Search** — Serper API
- **Paper Search** — arxiv API
- **UI** — Streamlit
- **Language** — Python 3.11

---

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/MishraNehal/AI-Research-Newsletter-Generator
cd AI-Research-Newsletter-Generator
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Add your API keys — create a `.env` file**
```
GEMINI_API_KEY=your_key_here
SERPER_API_KEY=your_key_here
MODEL=gemini/gemini-2.5-flash-lite
```

**4. Run**
```bash
# Command line
python -m ai_newsletter.main "multimodal AI"

# Streamlit UI
streamlit run streamlit_app.py
```

---

## Project Structure

```
ai_newsletter/
├── src/ai_newsletter/
│   ├── config/
│   │   ├── agents.yaml    ← agent prompts
│   │   └── tasks.yaml     ← task definitions
│   ├── tools/
│   │   ├── search_tool.py
│   │   └── arxiv_tool.py
│   ├── crew.py            ← crew definition
│   └── main.py            ← entry point
├── streamlit_app.py       ← UI
├── requirements.txt
└── .env                   ← API keys (not committed)
```

---

## API Keys Required

| Service | Free Tier | Link |
|---|---|---|
| Google Gemini | Yes | [aistudio.google.com](https://aistudio.google.com) |
| Serper | 2500 searches/month | [serper.dev](https://serper.dev) |

---

*Built with CrewAI · Gemini 2.5 Flash Lite · Serper · arxiv*