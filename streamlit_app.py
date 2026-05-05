"""
streamlit_app.py — Demo UI for AI Newsletter Crew
Place this file in the root of your project (same level as src/)
Run: streamlit run streamlit_app.py
"""

import streamlit as st
import sys
import os
import time
from datetime import datetime
from pathlib import Path

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Research Newsletter",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Custom CSS ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0A0A0A;
    color: #E8E3DC;
}

.main { background-color: #0A0A0A; }
.block-container { padding: 2rem 3rem; max-width: 900px; margin: auto; }

h1 { font-family: 'DM Serif Display', serif !important; font-size: 3rem !important; color: #E8E3DC !important; letter-spacing: -1px; }
h2, h3 { font-family: 'DM Serif Display', serif !important; color: #E8E3DC !important; }

.tagline {
    font-family: 'DM Mono', monospace;
    font-size: 12px;
    color: #C8A96E;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

.stTextInput > div > div > input {
    background: #141414 !important;
    border: 1px solid #2A2A2A !important;
    border-radius: 4px !important;
    color: #E8E3DC !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 16px !important;
    padding: 14px 18px !important;
}
.stTextInput > div > div > input:focus {
    border-color: #C8A96E !important;
    box-shadow: 0 0 0 1px #C8A96E !important;
}

.stButton > button {
    background: #C8A96E !important;
    color: #0A0A0A !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    border: none !important;
    border-radius: 4px !important;
    padding: 12px 32px !important;
    letter-spacing: 0.05em !important;
    width: 100%;
    transition: all 0.2s;
}
.stButton > button:hover {
    background: #D4B97E !important;
    transform: translateY(-1px);
}

.agent-card {
    background: #141414;
    border: 1px solid #2A2A2A;
    border-radius: 6px;
    padding: 14px 18px;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 14px;
}
.agent-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.agent-dot.idle { background: #333; }
.agent-dot.running { background: #C8A96E; animation: pulse 1s infinite; }
.agent-dot.done { background: #4CAF82; }
.agent-name { font-family: 'DM Mono', monospace; font-size: 13px; color: #E8E3DC; }
.agent-status { font-size: 12px; color: #666; margin-left: auto; }

@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.4} }

.newsletter-output {
    background: #141414;
    border: 1px solid #2A2A2A;
    border-radius: 6px;
    padding: 32px;
    margin-top: 24px;
    font-family: 'DM Sans', sans-serif;
    line-height: 1.8;
}

.divider {
    border: none;
    border-top: 1px solid #2A2A2A;
    margin: 24px 0;
}

.stat-row {
    display: flex;
    gap: 24px;
    margin: 16px 0;
}
.stat {
    background: #141414;
    border: 1px solid #2A2A2A;
    border-radius: 4px;
    padding: 12px 20px;
    text-align: center;
    flex: 1;
}
.stat-num { font-family: 'DM Serif Display', serif; font-size: 24px; color: #C8A96E; }
.stat-label { font-size: 11px; color: #666; text-transform: uppercase; letter-spacing: 0.1em; margin-top: 2px; }

.error-box {
    background: #1A0A0A;
    border: 1px solid #5C1A1A;
    border-radius: 6px;
    padding: 16px 20px;
    color: #FF6B6B;
    font-family: 'DM Mono', monospace;
    font-size: 13px;
}

.stDownloadButton > button {
    background: transparent !important;
    color: #C8A96E !important;
    border: 1px solid #C8A96E !important;
    border-radius: 4px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    padding: 8px 20px !important;
}
</style>
""", unsafe_allow_html=True)

# ── Add src to path so crew can be imported ─────────────────────────────────────
sys.path.insert(0, str(Path(__file__).parent / "src"))

# ── Header ──────────────────────────────────────────────────────────────────────
st.markdown('<div class="tagline">Powered by CrewAI × Groq</div>', unsafe_allow_html=True)
st.title("The AI Weekly Digest")
st.markdown("*Three specialized AI agents research, summarize, and edit the week's most important papers — automatically.*")

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Input ───────────────────────────────────────────────────────────────────────
col1, col2 = st.columns([4, 1])
with col1:
    topic = st.text_input(
        "",
        placeholder="Enter a research topic — e.g. 'multimodal AI', 'RAG systems', 'AI agents'",
        label_visibility="collapsed"
    )
with col2:
    generate = st.button("Generate →")

# ── Suggested topics ────────────────────────────────────────────────────────────
st.markdown('<p style="font-size:12px;color:#444;margin-top:8px">Suggested: &nbsp;', unsafe_allow_html=True)
suggestions = ["AI Agents", "LLM Reasoning", "Multimodal AI", "AI Safety", "RAG Systems"]
cols = st.columns(len(suggestions))
for i, s in enumerate(suggestions):
    with cols[i]:
        if st.button(s, key=f"sug_{i}"):
            topic = s
            generate = True

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Generation logic ────────────────────────────────────────────────────────────
if generate and topic:
    os.makedirs("outputs", exist_ok=True)

    # Agent status display
    st.markdown("### Running your crew")
    agents_info = [
        ("🔍", "Senior AI Research Scout", "Searching arxiv & web for top papers..."),
        ("📝", "Research Summarizer", "Writing structured TLDRs for each paper..."),
        ("✏️", "Newsletter Editor", "Assembling the final newsletter..."),
    ]

    placeholders = []
    for icon, name, desc in agents_info:
        ph = st.empty()
        ph.markdown(f"""
        <div class="agent-card">
            <div class="agent-dot idle"></div>
            <span class="agent-name">{icon} {name}</span>
            <span class="agent-status">Waiting...</span>
        </div>""", unsafe_allow_html=True)
        placeholders.append((ph, icon, name, desc))

    start_time = time.time()
    newsletter_text = None
    error_msg = None

    # Update researcher to running
    placeholders[0][0].markdown(f"""
    <div class="agent-card">
        <div class="agent-dot running"></div>
        <span class="agent-name">{placeholders[0][1]} {placeholders[0][2]}</span>
        <span class="agent-status">{placeholders[0][3]}</span>
    </div>""", unsafe_allow_html=True)

    try:
        from ai_newsletter.crew import AiNewsletter

        def run_crew():
            return AiNewsletter().crew().kickoff(inputs={
                "topic": topic,
                "current_year": str(datetime.now().year),
            })

        # Run with retry
        max_retries = 8
        for attempt in range(max_retries):
            try:
                result = run_crew()
                newsletter_text = result.raw
                break
            except Exception as e:
                if "rate_limit" in str(e).lower() and attempt < max_retries - 1:
                    wait = 60 * (attempt + 1)
                    st.toast(f"⏳ Rate limit hit. Waiting {wait}s... (attempt {attempt+1})")
                    time.sleep(wait)
                else:
                    raise

        # Mark all agents done
        for ph, icon, name, desc in placeholders:
            ph.markdown(f"""
            <div class="agent-card">
                <div class="agent-dot done"></div>
                <span class="agent-name">{icon} {name}</span>
                <span class="agent-status">✓ Done</span>
            </div>""", unsafe_allow_html=True)

        elapsed = round(time.time() - start_time)
        word_count = len(newsletter_text.split())

        # Save output
        with open("outputs/newsletter.md", "w", encoding="utf-8") as f:
            f.write(newsletter_text)

    except Exception as e:
        error_msg = str(e)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    if error_msg:
        st.markdown(f'<div class="error-box">❌ {error_msg}</div>', unsafe_allow_html=True)

    elif newsletter_text:
        # Stats row
        st.markdown(f"""
        <div class="stat-row">
            <div class="stat"><div class="stat-num">{elapsed}s</div><div class="stat-label">Generated in</div></div>
            <div class="stat"><div class="stat-num">{word_count}</div><div class="stat-label">Words</div></div>
            <div class="stat"><div class="stat-num">{round(word_count/200)}</div><div class="stat-label">Min read</div></div>
        </div>
        """, unsafe_allow_html=True)

        # Download button
        st.download_button(
            label="⬇ Download newsletter.md",
            data=newsletter_text,
            file_name=f"newsletter_{topic.replace(' ','_')}_{datetime.now().strftime('%Y%m%d')}.md",
            mime="text/markdown"
        )

        # Rendered newsletter
        st.markdown("### Preview")
        st.markdown('<div class="newsletter-output">', unsafe_allow_html=True)
        st.markdown(newsletter_text)
        st.markdown('</div>', unsafe_allow_html=True)

elif generate and not topic:
    st.warning("Please enter a topic first.")

# ── Footer ──────────────────────────────────────────────────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown(
    '<p style="font-size:11px;color:#333;text-align:center;font-family:DM Mono,monospace">'
    'Built with CrewAI · Groq LLaMA 3.3 70B · Serper · arxiv'
    '</p>',
    unsafe_allow_html=True
)