import json
import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL

genai.configure(api_key=GEMINI_API_KEY)

SUMMARY_PROMPT = """You are Notely AI, a meeting/lecture intelligence assistant.
Given the transcript below, return ONLY valid JSON (no markdown fences, no preamble)
with this exact structure:

{{
  "executive_summary": "2-3 sentence high-level summary",
  "detailed_summary": "a fuller paragraph summary",
  "key_highlights": ["point 1", "point 2"],
  "decisions": ["decision 1"],
  "action_items": [{{"task": "...", "owner": "unknown or name if mentioned"}}],
  "topics": ["topic 1", "topic 2"]
}}

Transcript:
{transcript}
"""


def summarize_transcript(transcript: str) -> dict:
    model = genai.GenerativeModel(GEMINI_MODEL)
    prompt = SUMMARY_PROMPT.format(transcript=transcript)
    response = model.generate_content(prompt)
    text = response.text.strip().replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {
            "executive_summary": text[:300],
            "detailed_summary": text,
            "key_highlights": [],
            "decisions": [],
            "action_items": [],
            "topics": [],
        }