import streamlit as st
import sys
import os
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

st.set_page_config(
    page_title="The AI Weekly Digest",
    page_icon="📰",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;1,400&family=JetBrains+Mono:wght@400;500&family=Outfit:wght@300;400;500&display=swap');
html,body,[class*="css"],.stApp{background-color:#080808!important;color:#E4DDD3!important;font-family:'Outfit',sans-serif!important}
.block-container{padding:3rem 2rem 4rem!important;max-width:800px!important}
.eyebrow{font-family:'JetBrains Mono',monospace;font-size:11px;color:#C9A84C;letter-spacing:.2em;text-transform:uppercase;margin-bottom:12px}
.main-title{font-family:'Playfair Display',Georgia,serif;font-size:3rem;font-weight:600;color:#E4DDD3;line-height:1.05;margin-bottom:8px}
.main-title span{color:#C9A84C;font-style:italic}
.subtitle{font-size:15px;color:#666;font-weight:300;line-height:1.6}
.divider{border:none;border-top:1px solid #1e1e1e;margin:28px 0}
.input-label{font-family:'JetBrains Mono',monospace;font-size:10px;color:#333;letter-spacing:.12em;text-transform:uppercase;margin-bottom:8px}
.stTextInput>div>div>input{background:#111!important;border:1px solid #222!important;border-radius:4px!important;color:#E4DDD3!important;font-family:'Outfit',sans-serif!important;font-size:16px!important;padding:14px 18px!important}
.stTextInput>div>div>input:focus{border-color:#C9A84C!important;box-shadow:0 0 0 1px rgba(201,168,76,.25)!important}
.stTextInput>div>div>input::placeholder{color:#333!important}
.stButton>button{background:#C9A84C!important;color:#000!important;font-family:'Outfit',sans-serif!important;font-weight:500!important;font-size:14px!important;border:none!important;border-radius:4px!important;padding:12px 32px!important;letter-spacing:.04em!important;width:100%!important}
.stButton>button:hover{background:#D4B96E!important}
.agent-box{background:#111;border:1px solid #1e1e1e;border-radius:6px;padding:13px 16px;margin-bottom:8px;display:flex;align-items:center;gap:12px;font-size:13px;color:#E4DDD3}
.agent-box.active{border-color:#C9A84C}
.agent-box.done{border-color:#1a3a2a}
.dot{width:7px;height:7px;border-radius:50%;background:#222;flex-shrink:0}
.dot.active{background:#C9A84C}
.dot.done{background:#3DAA72}
.agent-status{font-family:'JetBrains Mono',monospace;font-size:10px;color:#444;margin-left:auto}
.agent-status.active{color:#C9A84C}
.agent-status.done{color:#3DAA72}
.stat-row{display:flex;gap:10px;margin:16px 0}
.stat-card{background:#111;border:1px solid #1e1e1e;border-radius:6px;padding:14px;text-align:center;flex:1}
.stat-num{font-family:'Playfair Display',serif;font-size:26px;color:#C9A84C;display:block}
.stat-label{font-family:'JetBrains Mono',monospace;font-size:10px;color:#333;text-transform:uppercase;letter-spacing:.1em;margin-top:3px}
.newsletter-wrap{background:#111;border:1px solid #1e1e1e;border-radius:6px;padding:32px 36px;margin-top:20px;line-height:1.85}
.error-box{background:rgba(192,57,43,.07);border:1px solid rgba(192,57,43,.25);border-radius:6px;padding:14px 18px;color:#E57373;font-family:'JetBrains Mono',monospace;font-size:12px;margin-top:16px}
.stDownloadButton>button{background:transparent!important;color:#C9A84C!important;border:1px solid #C9A84C!important;font-size:13px!important;padding:8px 20px!important;width:auto!important}
.footer-custom{text-align:center;font-family:'JetBrains Mono',monospace;font-size:10px;color:#222;margin-top:48px;letter-spacing:.06em}
#MainMenu{visibility:hidden}header{visibility:hidden}footer{visibility:hidden}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="eyebrow">CrewAI · Groq · Serper · arxiv</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">The AI Weekly<br><span>Digest</span></div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Three AI agents research, summarize, and edit the week\'s most important papers.</div>', unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)

st.markdown('<div class="input-label">Research topic</div>', unsafe_allow_html=True)
topic = st.text_input("", placeholder="e.g. multimodal AI, RAG systems, AI agents... (leave blank for default)", label_visibility="collapsed")

generate = st.button("Generate →", use_container_width=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

if generate:
    final_topic = topic.strip() if topic.strip() else "AI LLMs and Agents"
    os.makedirs("outputs", exist_ok=True)

    def agent_html(icon, name, state="idle"):
        dot_cls = "dot active" if state=="active" else "dot done" if state=="done" else "dot"
        box_cls = "agent-box active" if state=="active" else "agent-box done" if state=="done" else "agent-box"
        status = "Running..." if state=="active" else "✓ Done" if state=="done" else "Waiting"
        status_cls = "agent-status active" if state=="active" else "agent-status done" if state=="done" else "agent-status"
        return f'<div class="{box_cls}"><div class="{dot_cls}"></div><span style="flex:1">{icon} {name}</span><span class="{status_cls}">{status}</span></div>'

    ph0 = st.empty()
    ph1 = st.empty()
    ph2 = st.empty()
    timer_ph = st.empty()

    ph0.markdown(agent_html("🔍","Senior AI Research Scout","active"), unsafe_allow_html=True)
    ph1.markdown(agent_html("📝","Research Summarizer","idle"), unsafe_allow_html=True)
    ph2.markdown(agent_html("✏️","Newsletter Editor","idle"), unsafe_allow_html=True)

    start = time.time()
    newsletter_text = None
    error_msg = None

    try:
        from ai_newsletter.crew import AiNewsletter
        inputs = {
            "topic": final_topic,
            "current_year": str(datetime.now().year),
            "current_date": datetime.now().strftime("%B %d, %Y"),
        }
        for attempt in range(8):
            try:
                timer_ph.markdown(f'<div style="font-family:JetBrains Mono,monospace;font-size:11px;color:#444">⏱ {round(time.time()-start)}s elapsed...</div>', unsafe_allow_html=True)
                result = AiNewsletter().crew().kickoff(inputs=inputs)
                newsletter_text = result.raw
                break
            except Exception as e:
                if "rate_limit" in str(e).lower() and attempt < 7:
                    timer_ph.markdown(f'<div style="font-family:JetBrains Mono,monospace;font-size:11px;color:#C9A84C">⏳ Rate limit — waiting 60s (retry {attempt+1}/7)</div>', unsafe_allow_html=True)
                    time.sleep(60)
                else:
                    raise

        ph0.markdown(agent_html("🔍","Senior AI Research Scout","done"), unsafe_allow_html=True)
        ph1.markdown(agent_html("📝","Research Summarizer","done"), unsafe_allow_html=True)
        ph2.markdown(agent_html("✏️","Newsletter Editor","done"), unsafe_allow_html=True)
        timer_ph.empty()

        elapsed = round(time.time()-start)
        word_count = len(newsletter_text.split())
        with open("outputs/newsletter.md","w",encoding="utf-8") as f:
            f.write(newsletter_text)

    except Exception as e:
        error_msg = str(e)
        timer_ph.empty()

    if error_msg:
        st.markdown(f'<div class="error-box">❌ {error_msg}</div>', unsafe_allow_html=True)
    elif newsletter_text:
        st.markdown(f"""
        <div class="stat-row">
            <div class="stat-card"><span class="stat-num">{elapsed}s</span><div class="stat-label">Generated in</div></div>
            <div class="stat-card"><span class="stat-num">{word_count}</span><div class="stat-label">Words</div></div>
            <div class="stat-card"><span class="stat-num">{max(1,round(word_count/200))}</span><div class="stat-label">Min read</div></div>
        </div>""", unsafe_allow_html=True)

        st.download_button(
            "⬇ Download newsletter.md",
            data=newsletter_text,
            file_name=f"newsletter_{final_topic.replace(' ','_')}_{datetime.now().strftime('%Y%m%d')}.md",
            mime="text/markdown"
        )
        st.markdown('<div class="newsletter-wrap">', unsafe_allow_html=True)
        st.markdown(newsletter_text)
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="footer-custom">Built with CrewAI · Groq LLaMA 3.3 70B · Serper · arxiv</div>', unsafe_allow_html=True)