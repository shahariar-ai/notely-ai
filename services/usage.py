"""Per-user daily usage cap on the shared Gemini key.

Counters live in the Supabase `usage` table (see supabase_usage.sql). If the table
does not exist yet (or Supabase errors), the cap is NOT enforced and a warning is
logged, so the app never breaks because of it.
"""
import logging
from datetime import datetime, timezone

from config import get_secret
from services.auth import get_client

log = logging.getLogger(__name__)

DEFAULT_LIMITS = {"transcribe": 5, "ai": 40}
LABELS = {"transcribe": "transcriptions", "ai": "AI actions"}


def _limit(kind: str) -> int:
    raw = get_secret(f"DAILY_{kind.upper()}_LIMIT")
    try:
        return int(raw) if raw else DEFAULT_LIMITS[kind]
    except (TypeError, ValueError):
        return DEFAULT_LIMITS[kind]


def check_and_consume(user_id: str, kind: str):
    """Return (allowed, message). Consumes one unit when allowed."""
    limit = _limit(kind)
    day = datetime.now(timezone.utc).date().isoformat()
    try:
        client = get_client()
        res = (
            client.table("usage").select("count")
            .eq("user_id", user_id).eq("day", day).eq("kind", kind).execute()
        )
        used = res.data[0]["count"] if res.data else 0
        if used >= limit:
            return False, (
                f"Daily limit reached: {limit} {LABELS[kind]} per day on the free plan. "
                "It resets at 00:00 UTC."
            )
        client.table("usage").upsert(
            {"user_id": user_id, "day": day, "kind": kind, "count": used + 1},
            on_conflict="user_id,day,kind",
        ).execute()
        return True, ""
    except Exception as e:  # table missing, network, RLS... never block the user
        log.warning("Usage cap not enforced (%s): %s", type(e).__name__, e)
        return True, ""
