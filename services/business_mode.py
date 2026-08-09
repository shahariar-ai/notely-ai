import json
import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL

genai.configure(api_key=GEMINI_API_KEY)

BUSINESS_PROMPT = """You are Notely AI's Business Mode assistant.
From the transcript below, generate ONLY valid JSON (no markdown fences) with:

{{
  "meeting_minutes": "formal Minutes of Meeting (MoM) text",
  "executive_report": "a report-style summary for leadership",
  "project_updates": ["update 1", "update 2"],
  "decision_log": [{{"decision": "...", "context": "..."}}],
  "follow_ups": [{{"task": "...", "owner": "...", "due": "unknown or date if mentioned"}}]
}}

Transcript:
{transcript}
"""


def generate_business_pack(transcript: str) -> dict:
    model = genai.GenerativeModel(GEMINI_MODEL)
    prompt = BUSINESS_PROMPT.format(transcript=transcript)
    response = model.generate_content(prompt)
    text = response.text.strip().replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {
            "meeting_minutes": text, "executive_report": "", "project_updates": [],
            "decision_log": [], "follow_ups": [],
        }