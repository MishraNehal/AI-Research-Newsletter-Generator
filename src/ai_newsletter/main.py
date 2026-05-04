#!/usr/bin/env python
import os
import sys
import time
from datetime import datetime
from ai_newsletter.crew import AiNewsletter

def run():
    os.makedirs("outputs", exist_ok=True)

    topic = sys.argv[1] if len(sys.argv) > 1 else "AI LLMs and Agents"
    inputs = {
        "topic": topic,
        "current_year": str(datetime.now().year),
    }

    print(f"\n🚀 Starting newsletter crew for topic: '{topic}'\n")
    print("─" * 50)

    max_retries = 8
    retry_wait = 60  # seconds to wait between retries

    for attempt in range(1, max_retries + 1):
        try:
            result = AiNewsletter().crew().kickoff(inputs=inputs)
            newsletter_text = result.raw

            with open("outputs/newsletter.md", "w", encoding="utf-8") as f:
                f.write(newsletter_text)

            print("\n" + "─" * 50)
            print("✅ Newsletter generated successfully!")
            print("📄 Saved to: outputs/newsletter.md")
            return

        except Exception as e:
            error_msg = str(e)
            if "rate_limit" in error_msg.lower() or "ratelimit" in error_msg.lower():
                if attempt < max_retries:
                    print(f"\n⏳ Rate limit hit. Waiting {retry_wait}s before retry {attempt}/{max_retries-1}...")
                    time.sleep(retry_wait)
                else:
                    print("\n❌ Rate limit hit too many times. Try again in a few minutes.")
            else:
                print(f"\n❌ Error: {e}")
                raise

if __name__ == "__main__":
    run()