import os 
import time
from ai_engine.ai_editor import editor
from db.chroma_setup import collection
class EditorAgent:
    def __init__(self):
        print("EditorAgent Starts...")
    def run(self, input_path,base_name):
        print(f"Editing the reviewed chapter: {input_path}")
        if not input_path or not os.path.exists(input_path):
            raise FileNotFoundError("Input file not found")
        final_path = editor(input_path,base_name)
        if not final_path or not os.path.exists(final_path):
            print("No manually edited file to save")
            return final_path
        with open(final_path,"r",encoding="utf-8")as f:
            manual_edited= f.read()
        doc_id = f"{base_name}_manual_edited_{int(time.time())}"
        collection.add(
             documents=[manual_edited],
            metadatas=[{
                "base_name": base_name,
                "version_type": "edited",
                "timestamp": time.strftime("%d-%m-%Y_%H:%M:%S"),
                "reward_score": 0
            }],
            ids=[doc_id]
        )
        print(f"manually edited file is saved to chromadb at:{doc_id}")
        print(f"Final output saved: {final_path}")
        return final_path
