from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def sign_up(email, password):
    return supabase.auth.sign_up({"email": email, "password": password})


def sign_in(email, password):
    return supabase.auth.sign_in_with_password({"email": email, "password": password})


def sign_out():
    supabase.auth.sign_out()


def get_client():
    return supabase