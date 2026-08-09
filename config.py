import os
from dotenv import load_dotenv

load_dotenv()
def get_secret(key):
    return os.getenv(key) or st.secrets.get(key, "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

DB_PATH = "data/notely.db"
AUDIO_DIR = "data/audio"
EXPORT_DIR = "data/exports"
GEMINI_MODEL = "gemini-flash-latest"
SUPABASE_AUDIO_BUCKET = "audio"