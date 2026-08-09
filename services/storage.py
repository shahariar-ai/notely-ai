from services.auth import get_client


def save_meeting(user_id, title, transcript, summary_dict, study_dict, audio_filename):
    client = get_client()
    client.table("meetings").insert({
        "user_id": user_id,
        "title": title,
        "transcript": transcript,
        "summary_json": summary_dict,
        "study_json": study_dict,
        "audio_filename": audio_filename,
    }).execute()


def get_all_meetings(user_id):
    client = get_client()
    res = client.table("meetings").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
    return res.data


def search_meetings(user_id, query):
    client = get_client()
    res = (
        client.table("meetings")
        .select("*")
        .eq("user_id", user_id)
        .ilike("transcript", f"%{query}%")
        .execute()
    )
    return res.data