import asyncio
import os
import re
import base64
from datetime import datetime
from urllib.parse import urlparse, unquote
from playwright.async_api import async_playwright
from db.chroma_setup import version_storage
def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'\s+', '_', text)
    return text[:100]
def extract_path_from_url(url: str) -> str:
    path = urlparse(url).path
    path_parts = path.strip("/").split("/")[1:]
    slug = "_".join([slugify(part) for part in path_parts])
    return slug
async def fetch_chapter_content(chapter_url: str) -> tuple[str,str]:
    print("Scraping started...")
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(chapter_url)
        try:
            title = await page.inner_text("h1")
            raw_content = await page.inner_text("div#mw-content-text")
        except Exception as e:
            print(f"Failed to extract content: {e}")
            return None
        def clean(text: str) -> str:
            text = re.sub(r'\[\s*edit\s*\]', '', text)
            text = re.sub(r'\[\d+\]', '', text)
            text = re.sub(r'\n\s*\n+', '\n\n', text)
            return text.strip()
        content = clean(raw_content)
        filename_base = extract_path_from_url(chapter_url)
        timestamp = datetime.now().strftime("%d%m%Y_%H%M%S")
        text_path = os.path.join(data_dir, f"{filename_base}_{timestamp}.txt")
        screenshot_path = os.path.join(data_dir, f"{filename_base}_{timestamp}.png")
        with open(text_path, "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\n{content}")
        await page.screenshot(path=screenshot_path, full_page=True)
        await browser.close()
        print(f"Content text saved: {text_path}")
        print(f"Screenshot saved: {screenshot_path}")
        with open(text_path, "r", encoding="utf-8") as f:
            raw_text = f.read()
        with open(screenshot_path, "rb") as img_file:
            screenshot_b64 = base64.b64encode(img_file.read()).decode("utf-8")
        version_storage(
            content=raw_text,
            base_name=filename_base,
            version_type="raw",
            score=0.0,
            extra_metadata={
                "timestamp": timestamp,
                "screenshot_b64": screenshot_b64,
                  "title":title,
                    "source_url":chapter_url
            }
        )
        return text_path,filename_base
