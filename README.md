# ClipNarrator

🎬 ClipNarrator — AI Shorts Script Generator (Streamlit)

## About
ClipNarrator generates short, punchy scripts for YouTube Shorts and Reels using editable templates and an LLM backend.

This repository contains the Day-1 UI scaffold (Streamlit) and template loader. Replace the `generate_script()` stub in `app.py` with your model inference to enable full functionality.

## Quick start (local)
```bash
python -m venv .venv
source .venv/bin/activate      # on macOS / Linux
.venv\Scripts\activate         # on Windows

pip install -r requirements.txt
streamlit run app.py
