﻿# Automated Book Publication Workflow

This project is a modular, CLI-based AI-driven system for scraping and transforming public domain book chapters (e.g., from Wikisource) into refined versions using LLMs, with manual feedback loops and version control.

---

###  Features

-  **Web Scraping**: Extracts chapter content and screenshots using Playwright.
-  **AI Writing**: Rewrites chapters with better clarity while preserving the original meaning.
-  **Review & Edit**: Human-in-the-loop enabled AI refinement through separate agents.
-  **Versioning**: Stores each version (rewritten, reviewed, edited) in ChromaDB with timestamps.
-  **RL-Based Selection**: Chooses the best version using a reward scoring system.

---

###  Technologies Used

- Python
- Playwright
- Ollama (LLaMA3 model)
- ChromaDB
- Simple RL (score-based) selector

---

###  How to Run (CLI Only)

```bash
# Step into the environment
cd automated-book-pub

# Activate your venv if not already
# On Windows:
.\venv\Scripts\activate

# Run the main agentic pipeline
python agentic_api/agent_controller.py

```
### for reference
video:https://drive.google.com/file/d/1oQH6Rr9TSJzFVLMLRwMYwPdJxASpVme6/view?usp=sharing
github:https://github.com/Sriharisudhan26/automated-book-publication-workflow
