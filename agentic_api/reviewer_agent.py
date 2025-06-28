import os
import time
from db.chroma_setup import collection
from ai_engine.reviewer import reviewer
class ReviewerAgent:
    def __init__(self):
        print("ReviewerAgent Started...")
    def run(self, input_path,base_name):
        print("Reviewing the rewritten chapter...")
        reviewer_path = reviewer(input_path,base_name)
        if not reviewer_path or not os.path.exists(reviewer_path):
            raise FileNotFoundError("ReviewerAgent fails...")
        with open(reviewer_path, "r", encoding="utf-8") as f:
            manual_edited = f.read()
        doc_id = f"{base_name}_manual_reviewed_{int(time.time())}"
        collection.add(
            documents=[manual_edited],
            metadatas=[{
                "base_name": base_name,
                "version_type": "reviewed",
                "timestamp": time.strftime("%d-%m-%Y_%H:%M:%S"),
                "reward_score": 0
            }],
            ids=[doc_id]
        )
        print(f"manually edited file is saved to chromadb at:{doc_id}")
        print(f"Reviewed Output:{reviewer_path}")
        return reviewer_path
