import os
import time
from ai_engine.summarizer import summarizer
from db.chroma_setup import collection
class SummarizerAgent:
    def __init__(self):
        print("SummarizerAgent Initialized...")
    def run(self, input_path,base_name):
        print(f"Summarizing: {input_path}")
        if not input_path or not os.path.exists(input_path):
            raise FileNotFoundError("Input path does not exist.")
        output_path = summarizer(input_path,base_name)
        if not output_path or not os.path.exists(output_path):
            print("Summary file not generated.")
            return output_path
        print("You may now review and edit the summary if wanted.")
        input("After editing, press Enter to continue...")
        with open(output_path, "r", encoding="utf-8") as f:
            manual_edited = f.read()
        doc_id = f"{base_name}_manual_summary_{int(time.time())}"
        collection.add(
            documents=[manual_edited],
            metadatas=[{
                "base_name": base_name,
                "version_type": "summary",
                "timestamp": time.strftime("%d-%m-%Y_%H:%M:%S"),
                "reward_score": 0
            }],
            ids=[doc_id]
        )
        print(f"manually edited file is saved to chromadb at:{doc_id}")
        print(f"Summary saved at: {output_path}")
        return input_path 