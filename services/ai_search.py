import json
import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL

genai.configure(api_key=GEMINI_API_KEY)


def ai_search(query: str, meetings: list) -> list:
    if not meetings:
        return []

    catalog = [
        {
            "id": m["id"],
            "title": m.get("title", ""),
            "summary": (m.get("summary_json") or {}).get("executive_summary", ""),
        }
        for m in meetings
    ]

    prompt = f"""You are a search assistant. Given this list of meetings (JSON) and a
user query, return ONLY a JSON array of the "id" values of meetings that match
the query's intent. If nothing matches, return [].

Meetings:
{json.dumps(catalog)}

Query: {query}
"""
    model = genai.GenerativeModel(GEMINI_MODEL)
    response = model.generate_content(prompt)
    text = response.text.strip().replace("```json", "").replace("```", "").strip()

    try:
        matched_ids = set(json.loads(text))
    except json.JSONDecodeError:
        return meetings

    return [m for m in meetings if m["id"] in matched_ids]