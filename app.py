# app.py (simplified ClipNarrator UI)
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import textwrap
import time

# ---------- CONFIG ----------
APP_TITLE = "ClipNarrator"
APP_SUBTITLE = "AI Shorts Script Generator"
PROJECT_DIR = Path(__file__).parent
TEMPLATES_DIR = PROJECT_DIR / "templates"

# ---------- UTILITIES ----------
def load_templates():
    TEMPLATES_DIR.mkdir(exist_ok=True)
    templates = {}
    for p in sorted(TEMPLATES_DIR.glob("*.txt")):
        templates[p.stem] = p.read_text(encoding="utf-8")
    if not templates:
        templates = {
            "facts": textwrap.dedent("""\
                Hook: One-line punchy hook.
                Fact 1: Short surprising fact.
                Fact 2: Short surprising fact.
                Fact 3: Short surprising fact.
                Closing: Quick CTA or punchline.
            """),
            "motivation": textwrap.dedent("""\
                Hook: Relatable opening line.
                Point 1: Short tip or story.
                Point 2: Practical advice.
                Closing: Strong one-liner CTA.
            """),
            "tech": textwrap.dedent("""\
                Hook: The problem in one line.
                Explain: 2-3 short lines.
                Example: One short example.
                Takeaway: What to remember + CTA.
            """)
        }
    return templates

def generate_script(topic: str, template_text: str, length_words: int = 80):
    """Simple placeholder generator — replace with model call later."""
    time.sleep(0.4)
    lines = []
    for line in template_text.splitlines():
        if not line.strip():
            continue
        key = line.split(":",1)[0].strip().lower()
        if "hook" in key:
            lines.append(f"Hook: {topic} — here's the one thing you must know.")
        elif any(k in key for k in ("fact","point","explain","example")):
            lines.append(f"{line.split(':',1)[0]}: A short point about {topic}.")
        elif any(k in key for k in ("closing","takeaway")):
            lines.append(f"{line.split(':',1)[0]}: If you remember one thing — {topic}.")
        else:
            lines.append(line)
    script = "\n".join(lines)
    words = script.split()
    if len(words) > length_words:
        script = " ".join(words[:length_words]) + "..."
    return script

# ---------- UI ----------
st.set_page_config(page_title=APP_TITLE, page_icon="🎬", layout="centered")
st.title(APP_TITLE)
st.write(APP_SUBTITLE)

# Simple top controls
templates = load_templates()
style = st.selectbox("Choose style", list(templates.keys()))
topic = st.text_input("Topic (what is the short about?)", "")
length = st.select_slider("Target length (words)", options=[30,50,80,110], value=80)

st.markdown("**Template (edit if you want custom output)**")
template_editor = st.text_area("Template", value=templates[style], height=160)

cols = st.columns([1,1])
with cols[0]:
    if st.button("Generate"):
        if not topic.strip():
            st.warning("Please enter a topic.")
        else:
            with st.spinner("Generating..."):
                draft = generate_script(topic.strip(), template_editor, length_words=length)
                st.session_state["script"] = draft
                st.success("Draft ready.")
with cols[1]:
    if st.button("Regenerate"):
        if not topic.strip():
            st.warning("Please enter a topic.")
        else:
            with st.spinner("Regenerating..."):
                draft = generate_script(topic.strip(), template_editor, length_words=length)
                st.session_state["script"] = draft
                st.success("Regenerated.")

st.markdown("---")
script_text = st.session_state.get("script", "Your generated script will appear here after you click Generate.")
st.code(script_text, language="text")

# Safe copy button using escaped string
copy_html = f"""
<div style="margin-top:6px;">
  <button id="copy-btn" style="padding:8px 12px;border-radius:6px;border:1px solid #ccc;cursor:pointer;">
    Copy to clipboard
  </button>
</div>
<script>
  const btn = document.getElementById("copy-btn");
  btn.addEventListener("click", () => {{
    navigator.clipboard.writeText({script_text!r});
    btn.innerText = "Copied!";
    setTimeout(()=>{{ btn.innerText = "Copy to clipboard"; }}, 1500);
  }});
</script>
"""
components.html(copy_html, height=70)

# Download button
st.download_button("Download .txt", data=script_text, file_name="clipnarrator_script.txt")

# Small support button (Ko-fi)
kofi_html = """
<div style="text-align:center;margin-top:10px;">
  <a href="https://ko-fi.com/yourname" target="_blank">
    <img height="36" style="border:0;" src="https://cdn.ko-fi.com/cdn/kofi5.png" alt="Buy Me a Coffee" />
  </a>
</div>
"""
components.html(kofi_html, height=60)
