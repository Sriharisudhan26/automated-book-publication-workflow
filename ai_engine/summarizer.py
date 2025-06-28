import os
import ollama
from datetime import datetime
from db.chroma_setup import version_storage
def summarizer(chapter_path: str, base_name: str):
    if not os.path.exists(chapter_path):
        print("File not found:", chapter_path)
        return None
    with open(chapter_path, "r", encoding="utf-8") as file:
        chapter_text = file.read()

    prompt = f"""
please help me to summarize the following chapter into proper paragraph.
Do it as assistant to help me.

Chapter:
\"\"\"{chapter_text}\"\"\"

Output only the summary paragraph. Avoid bulletins or notes.
"""

    try:
        response = ollama.chat(
            model="llama3",
            messages=[{"role": "user", "content": prompt}]
        )
        summary = response["message"]["content"]
    except Exception as e:
        print("Error in summarizing,Ollama fails.", e)
        return
    today = datetime.today().strftime("%d-%m-%Y")
    output_dir = os.path.join("output", today)
    os.makedirs(output_dir, exist_ok=True)
    summary_path = os.path.join(output_dir, f"{base_name}_summary.txt")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(summary.strip())
    print("Summary saved:", summary_path)
    #db
    version_storage(content=summary.strip(), base_name=base_name, version_type="summary", score=0.0)
    #db
    print("You may now review and edit the summary if wamted.")
    input("After editing press enter to continue...")
    print("Proceeding to next step...")
    return summary_path