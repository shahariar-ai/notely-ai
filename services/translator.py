import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL

genai.configure(api_key=GEMINI_API_KEY)


def translate_text(text: str, target_language: str) -> str:
    model = genai.GenerativeModel(GEMINI_MODEL)
    prompt = (
        f"Translate the following text into {target_language}. "
        "Preserve meaning and tone. Return only the translated text, "
        "no notes or explanations.\n\nText:\n" + text
    )
    response = model.generate_content(prompt)
    return response.text.strip()