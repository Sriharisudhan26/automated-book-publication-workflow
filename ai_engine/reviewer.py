import os
import re
import ollama
from datetime import datetime
from db.chroma_setup import version_storage
def reviewer(input_path: str,base_name:str):
    print("Reviewing process started...")
    if not os.path.exists(input_path):
        print("Input file not found:", input_path)
        return None
    print("Rewritten file loaded for review:", input_path)
    with open(input_path, "r", encoding="utf-8") as f:
        chapter_text = f.read()
    prompt = f"""help me to refine and review the content given by make the grammar errors, improve the quality of content without changing its core meaning.
ensure not losing its originality. Add the title and heading into if needs

content:
{chapter_text}
"""
    try:
        response = ollama.chat(
            model="llama3",
            messages=[{"role": "user", "content": prompt}]
        )
        reviewed_text = response["message"]["content"]
    except Exception as e:
        print("Unable to proceed,Ollama failed to review", e)
        return None
    timestamp = datetime.now().strftime("%d-%m-%Y_%H%M%S")
    reviewed_path = os.path.join("data", f"{base_name}_final_{timestamp}.txt")
    with open(reviewed_path, "w", encoding="utf-8") as f:
        f.write(reviewed_text.strip())
    print("Reviewed content available at:", reviewed_path)
    #db
    version_storage(content=reviewed_text.strip(), base_name=base_name, version_type="reviewed", score=0.0)
    #db
    print("You may now review and edit this file")
    input("After editing,press enter to continue...")
    print("Proceeding to next step...")
    return reviewed_path