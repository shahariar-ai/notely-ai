import json
import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL

genai.configure(api_key=GEMINI_API_KEY)

STUDY_PROMPT = """You are Notely AI's Study Mode assistant for students.
From the transcript below, generate ONLY valid JSON (no markdown fences) with:

{{
  "lecture_notes": "well-structured notes in your own words",
  "chapter_summary": "a concise chapter-style summary",
  "key_concepts": ["concept 1", "concept 2"],
  "definitions": [{{"term": "...", "definition": "..."}}],
  "flashcards": [{{"question": "...", "answer": "..."}}],
  "mcqs": [{{"question": "...", "options": ["A", "B", "C", "D"], "correct_answer": "A"}}]
}}

Transcript:
{transcript}
"""


def generate_study_pack(transcript: str) -> dict:
    model = genai.GenerativeModel(GEMINI_MODEL)
    prompt = STUDY_PROMPT.format(transcript=transcript)
    response = model.generate_content(prompt)
    text = response.text.strip().replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {
            "lecture_notes": text, "chapter_summary": "", "key_concepts": [],
            "definitions": [], "flashcards": [], "mcqs": [],
        }