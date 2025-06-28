import os
import ollama
from datetime import datetime
from db.chroma_setup import version_storage
def editor(input_path: str,base_name:str):
    if not os.path.exists(input_path):
        print("File not found:", input_path)
        return
    print("Editing process started...")
    print("reviewed chapter loaded:", input_path)
    with open(input_path, "r", encoding="utf-8") as file:
        content = file.read()
    prompt = f"""
I am assigning you as an editor for me to improve the reviewed content without losing its tone, flow, clarity and structure. Do it as a professional editor not like an AI trained.

no removal or addition of sections. provide the best version to me 

Contenr:
\"\"\"{content}\"\"\"
"""

    print("Sending to Ollama for final editing...")
    try:
        response = ollama.chat(
            model="llama3",
            messages=[{"role": "user", "content": prompt}]
        )
        edited_text = response["message"]["content"]
    except Exception as e:
        print("Error while editing,Ollama fails.", e)
        return
    timestamp = datetime.now().strftime("%d-%m-%Y_%H%M%S")
    final_name = f"{base_name}_edited_{timestamp}.txt"
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, final_name)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(edited_text.strip())
    print(f"Final refined version saved at: {output_path}")
    #db
    version_storage(content=edited_text.strip(), base_name=base_name, version_type="edited", score=0.0)
    #db
    print("Manual editing is now enabled. You may now open and fine-tune the file.")
    input("Press Enter after corrections to continue...")
    print("Editing completed.\n")
    return output_path