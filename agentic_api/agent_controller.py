import asyncio
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scraper.playwright_scraper import fetch_chapter_content
from agentic_api.writer_agent import WriterAgent
from agentic_api.summarizer_agent import SummarizerAgent
from agentic_api.reviewer_agent import ReviewerAgent
from agentic_api.editor_agent import EditorAgent
from rl.rl_selector import rl_version

async def run_pipeline():
    print("run_pipeline started\n")
    print("Enter content URL: ", end='', flush=True)
    url = input().strip()

    if not url:
        print("Invalid input.Exiting...")
        return

    print("Fetching content...")
    scraped_path,base_name = await fetch_chapter_content(url)
    if not scraped_path or not os.path.exists(scraped_path):
        print("Scraping failed")
        return
    print(f"Scraping successful: {scraped_path}")

    writer = WriterAgent()
    rewritten_path = writer.run(scraped_path,base_name)

    summarizer = SummarizerAgent()
    summarized_path = summarizer.run(rewritten_path,base_name)

    reviewer = ReviewerAgent()
    reviewed_path = reviewer.run(summarized_path,base_name)

    editor = EditorAgent()
    final_path = editor.run(reviewed_path,base_name)
    print("\nSelecting best version by Reinforcement process")
    best = rl_version(base_name)
    if best:
        score = {best['metadata'].get('reward_score',0)}
        print("\nBest version selected")
        print(f"ID : {best['id']}")
        print(f"Score :{score}")
        if score ==0:
            print("Best version has 0 as score as it is the first run. To allocate manual rating for each version, try running score_update.py")
    else:
        print("No score versions found:",base_name)
    
    print(f"\nPipeline completed successfully.")

asyncio.run(run_pipeline())