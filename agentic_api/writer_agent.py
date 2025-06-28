import os
from ai_engine.chapter_generator import generate_chapter
class WriterAgent:
    def __init__(self):
        print("WriterAgent Initialized\n")
    def run(self, input_path,base_name):
        print("WriterAgent starts generating rewritten content...")
        print(f"writing started\nfound latest raw: {input_path}")
        rewritten_path = generate_chapter(input_path,base_name)
        if not rewritten_path or not os.path.exists(rewritten_path):
            raise FileNotFoundError("Failed to generate content")
        print(f"Output after rewriting: {rewritten_path}")
        return rewritten_path
