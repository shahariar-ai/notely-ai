import mimetypes
import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL

genai.configure(api_key=GEMINI_API_KEY)


def transcribe_audio(file_path: str) -> str:
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type:
        mime_type = "audio/wav"

    with open(file_path, "rb") as f:
        audio_bytes = f.read()

    model = genai.GenerativeModel(GEMINI_MODEL)
    prompt = (
        "Transcribe this audio completely and accurately. "
        "Identify distinct speakers by their voice and label them consistently "
        "throughout (Speaker 1, Speaker 2, etc.) — the same person must always "
        "get the same label, even if they speak multiple times. "
        "If any speaker states or is addressed by their actual name during the "
        "conversation, use that name instead of 'Speaker N' for all their lines. "
        "Include natural paragraph breaks between speaker turns. "
        "Return only the transcript text, no extra commentary."
    )

    response = model.generate_content([
        prompt,
        {"mime_type": mime_type, "data": audio_bytes},
    ])
    return response.text.strip()