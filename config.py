import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def get_secret(key):
    return os.getenv(key) or st.secrets.get(key, "")

GEMINI_API_KEY = get_secret("GEMINI_API_KEY")
SUPABASE_URL = get_secret("SUPABASE_URL")
SUPABASE_KEY = get_secret("SUPABASE_KEY")

DB_PATH = "data/notely.db"
AUDIO_DIR = "data/audio"
EXPORT_DIR = "data/exports"
GEMINI_MODEL = "gemini-flash-latest"
SUPABASE_AUDIO_BUCKET = "audio"