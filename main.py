import os
import asyncio
from datetime import datetime
from scraper.playwright_scraper import fetch_chapter_content
from ai_engine.chapter_generator import generate_chapter
from ai_engine.summarizer import summarizer
from ai_engine.reviewer import reviewer
from ai_engine.ai_editor import editor
def get_latest_scraped_file():
    os.makedirs("data",exist_ok=True)
    candidates = [f for f in os.listdir("data") if f.startswith("chapter1_") and f.endswith(".txt") and "rewritten" not in f]
    if not candidates:
        print("No scraped .txt found")
        return None
    latest = max(candidates,key=lambda f:os.path.getmtime(os.path.join("data",f)))
    return os.path.join("data",latest)

def pipeline():
    print("\n Starting pipeling:\n")
    url = input("Enter URL:").strip()
    print("Scraping starts")
    scarped_path = asyncio.run(fetch_chapter_content(url))
    if not scarped_path or not os.path.exists(scarped_path):
        print("Scarping Failed.")
        return
    print(f"Scraped file saved:{scarped_path}")
    print("\nRewriting chapter begins...")
    rewritten_path = generate_chapter()
    if not rewritten_path:
        print("Rewritten prcoess failed,Exiting...")
        return
    print("Summarizing the rewritten chapter...")
    summarizer(rewritten_path)
    print("\nReviewing the rewritten chapter...")
    reviewed_path = reviewer()
    if not reviewed_path:
        print("failed reviewing,Exiting")
        return
    print("\nManual editing for the latest AI reviewed")
    editor(reviewed_path)
    print("\n Pipeline completed successfully.")
if __name__ == "__main__":
    pipeline()