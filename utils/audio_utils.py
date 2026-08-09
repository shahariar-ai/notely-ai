import os
from config import AUDIO_DIR, SUPABASE_AUDIO_BUCKET
from services.auth import get_client


def save_uploaded_file(uploaded_file) -> str:
    os.makedirs(AUDIO_DIR, exist_ok=True)
    path = os.path.join(AUDIO_DIR, uploaded_file.name)
    with open(path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return path


def save_recorded_audio(audio_bytes: bytes, filename: str) -> str:
    os.makedirs(AUDIO_DIR, exist_ok=True)
    path = os.path.join(AUDIO_DIR, filename)
    with open(path, "wb") as f:
        f.write(audio_bytes)
    return path


def upload_audio_to_cloud(local_path: str, user_id: str) -> str:
    client = get_client()
    filename = f"{user_id}/{os.path.basename(local_path)}"
    with open(local_path, "rb") as f:
        client.storage.from_(SUPABASE_AUDIO_BUCKET).upload(
            filename, f, {"content-type": "audio/wav", "upsert": "true"}
        )
    return client.storage.from_(SUPABASE_AUDIO_BUCKET).get_public_url(filename)