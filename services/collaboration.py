from services.auth import get_client


def share_meeting(meeting_id: str, owner_id: str, email_to_share: str):
    client = get_client()
    res = client.table("meetings").select("shared_with").eq("id", meeting_id).eq("user_id", owner_id).execute()
    if not res.data:
        raise Exception("Meeting not found or you don't own it")

    current = res.data[0].get("shared_with") or []
    if email_to_share not in current:
        current.append(email_to_share)

    client.table("meetings").update({"shared_with": current}).eq("id", meeting_id).execute()


def unshare_meeting(meeting_id: str, owner_id: str, email_to_remove: str):
    client = get_client()
    res = client.table("meetings").select("shared_with").eq("id", meeting_id).eq("user_id", owner_id).execute()
    if not res.data:
        raise Exception("Meeting not found or you don't own it")

    current = [e for e in (res.data[0].get("shared_with") or []) if e != email_to_remove]
    client.table("meetings").update({"shared_with": current}).eq("id", meeting_id).execute()


def get_shared_with_me(user_email: str):
    client = get_client()
    res = client.table("meetings").select("*").contains("shared_with", [user_email]).execute()
    return res.data