import os
from datetime import datetime
import ollama
from db.chroma_setup import version_storage
def generate_chapter(input_path: str,base_name:str):
    print("rewriting process started...")
    if not os.path.exists(input_path):
        print("Input file not found:", input_path)
        return None
    with open(input_path, "r", encoding="utf-8") as f:
        original_text = f.read()

    prompt = f"""
I am assigning you as an assistant who rewrites the content given into a clear and precise without losing the originality and structure of the content.

Rewrite the following content:
{original_text}
"""

    print("Sending rewrite request to Ollama...")
    try:
        response = ollama.chat(
            model="llama3",
            messages=[{"role": "user", "content": prompt}]
        )
        rewritten = response["message"]["content"]
    except Exception as e:
        print("Error while rewriting,Ollama fails.", e)
        return None
    timestamp = datetime.now().strftime("%d-%m-%Y_%H%M%S")
    output_file = os.path.join("data", f"{base_name}_rewritten_{timestamp}.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(rewritten.strip())
    print("Rewritten chapter saved as:",{output_file})
    #db
    version_storage(content=rewritten.strip(),base_name=base_name,version_type="rewritten",score=0.0)
    return output_file