"""
api.py — FastAPI backend for AI Newsletter Crew
Place in root of project (same level as src/)
Run: uvicorn api:app --reload --port 8000
"""

import os
import sys
import time
import asyncio
from datetime import datetime
from pathlib import Path
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

app = FastAPI(title="AI Newsletter Crew API", version="1.0.0")

# CORS — allow frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static frontend files
frontend_path = Path(__file__).parent / "frontend"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")


# ── Request/Response models ────────────────────────────────────────────────────

class GenerateRequest(BaseModel):
    topic: str


class GenerateResponse(BaseModel):
    success: bool
    newsletter: str
    topic: str
    elapsed_seconds: float
    word_count: int
    generated_at: str
    error: str = ""


# ── Routes ─────────────────────────────────────────────────────────────────────

@app.get("/")
async def serve_frontend():
    """Serve the HTML frontend."""
    index = Path(__file__).parent / "frontend" / "index.html"
    if index.exists():
        return FileResponse(str(index))
    return {"message": "AI Newsletter API running", "docs": "/docs"}


@app.get("/health")
async def health():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}


@app.post("/generate", response_model=GenerateResponse)
async def generate_newsletter(request: GenerateRequest):
    """
    Generate a newsletter for the given topic.
    Runs the full CrewAI pipeline synchronously.
    """
    if not request.topic.strip():
        raise HTTPException(status_code=400, detail="Topic cannot be empty")

    os.makedirs("outputs", exist_ok=True)
    start_time = time.time()

    try:
        from ai_newsletter.crew import AiNewsletter

        inputs = {
            "topic": request.topic.strip(),
            "current_year": str(datetime.now().year),
            "current_date": datetime.now().strftime("%B %d, %Y"),  
        }

        # Run with retry for rate limits
        max_retries = 8
        newsletter_text = None

        for attempt in range(max_retries):
            try:
                result = await asyncio.to_thread(
                    lambda: AiNewsletter().crew().kickoff(inputs=inputs)
                )
                newsletter_text = result.raw
                break
            except Exception as e:
                if "rate_limit" in str(e).lower() and attempt < max_retries - 1:
                    wait = 60
                    await asyncio.sleep(wait)
                else:
                    raise

        # Save output file
        filename = f"outputs/newsletter_{request.topic.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(newsletter_text)

        elapsed = round(time.time() - start_time, 2)

        return GenerateResponse(
            success=True,
            newsletter=newsletter_text,
            topic=request.topic,
            elapsed_seconds=elapsed,
            word_count=len(newsletter_text.split()),
            generated_at=datetime.now().isoformat(),
        )

    except Exception as e:
        elapsed = round(time.time() - start_time, 2)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/history")
async def get_history():
    """Return list of previously generated newsletters."""
    outputs_dir = Path("outputs")
    if not outputs_dir.exists():
        return {"newsletters": []}

    files = sorted(outputs_dir.glob("*.md"), key=lambda f: f.stat().st_mtime, reverse=True)
    newsletters = []
    for f in files[:10]:  # last 10
        newsletters.append({
            "filename": f.name,
            "size_bytes": f.stat().st_size,
            "created_at": datetime.fromtimestamp(f.stat().st_mtime).isoformat(),
        })
    return {"newsletters": newsletters}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)