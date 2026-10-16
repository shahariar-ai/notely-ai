import logging

from config import SUPABASE_AUDIO_BUCKET
from services.auth import get_client

log = logging.getLogger(__name__)


def delete_user_data(user_id: str) -> dict:
    """Delete a user's meetings, stored audio and usage counters.

    The sign-in account itself can't be removed with the public key; users who also
    want the account removed email support (see the Privacy page).
    """
    client = get_client()
    result = {"audio_files": 0, "meetings": 0}

    try:
        bucket = client.storage.from_(SUPABASE_AUDIO_BUCKET)
        names = [f"{user_id}/{o['name']}" for o in bucket.list(user_id) if o.get("name")]
        if names:
            bucket.remove(names)
        result["audio_files"] = len(names)
    except Exception as e:
        log.warning("Audio deletion failed: %s", e)
        raise

    res = client.table("meetings").delete().eq("user_id", user_id).execute()
    result["meetings"] = len(res.data or [])

    try:
        client.table("usage").delete().eq("user_id", user_id).execute()
    except Exception as e:  # table may not exist yet
        log.warning("Usage rows not deleted: %s", e)
    return result
