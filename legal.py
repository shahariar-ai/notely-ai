import streamlit as st

SUPPORT_EMAIL = "shahriar.sharif406@gmail.com"
UPDATED = "October 2026"

PRIVACY = f"""
# Privacy Policy
_Last updated: {UPDATED}_

Notely AI turns recordings of meetings and lectures into transcripts, summaries and study material.

### What we collect
- **Account data:** your email address and a password (handled by Supabase Authentication).
- **Content you give us:** audio you upload or record, and the transcripts, summaries and
  other results generated from it.
- **Usage counters:** how many AI requests you make per day, to keep the free service fair.

### How it is processed
- **Audio and text are sent to Google Gemini** to produce transcripts, summaries, translations,
  study packs and answers. Google processes this data under its own terms and privacy policy.
- **Everything you save is stored in Supabase** (database and file storage): your meetings,
  transcripts, summaries and uploaded or recorded audio.
- We do not sell your data and we do not show ads.

### Sharing
Meetings are private to you. They are visible to others only when you explicitly share a meeting
with their email address, and you can unshare at any time.

### Your control
- **Delete my data:** use the *Delete my data* button on this page to permanently delete all your
  meetings, stored audio and usage counters.
- To also delete your sign-in account, or for any privacy request, email **{SUPPORT_EMAIL}**.

### Recordings and consent
Only record people who know they are being recorded. You are responsible for getting any consent
required where you live.

### Contact
{SUPPORT_EMAIL}
"""

TERMS = f"""
# Terms of Service
_Last updated: {UPDATED}_

By using Notely AI you agree to these terms.

1. **The service.** Notely AI provides AI-generated transcripts, summaries and study material from
   audio you provide. It is offered as is, and is currently free with daily usage limits.
2. **Accuracy.** AI output can contain mistakes. Check important details (names, numbers, decisions)
   before relying on them. Do not use it as the sole basis for legal, medical or financial decisions.
3. **Your content.** You keep ownership of your recordings and results. You give us permission to
   process them (including by Google Gemini) and store them (in Supabase) only to run the service for you.
4. **Acceptable use.** Do not upload content you have no right to use, record people without any
   required consent, break the law, or try to abuse, overload or bypass the usage limits.
5. **Availability.** We may change, limit or stop the service at any time, and we may suspend
   accounts that abuse it.
6. **Liability.** To the extent the law allows, Notely AI is not liable for losses arising from use
   of the service or from errors in its output.
7. **Data.** See the Privacy Policy. You can delete your data at any time.
8. **Contact.** {SUPPORT_EMAIL}
"""


def render_legal(page: str, user_id: str | None = None):
    """Render the 'privacy' or 'terms' page. user_id enables the Delete my data button."""
    if st.button("← Back to app"):
        st.session_state.page = "app"
        st.rerun()

    st.markdown(PRIVACY if page == "privacy" else TERMS)

    if page == "privacy":
        st.markdown("---")
        st.subheader("Delete my data")
        if user_id is None:
            st.caption("Log in to delete your data.")
            return
        st.warning("This permanently deletes all your meetings, stored audio and usage counters. It cannot be undone.")
        confirm = st.checkbox("I understand this cannot be undone", key="confirm_delete")
        if st.button("🗑️ Delete my data", disabled=not confirm):
            from services.data_deletion import delete_user_data
            try:
                res = delete_user_data(user_id)
                for k in ("last_transcript", "last_summary", "last_title", "exports",
                          "last_study", "last_business", "chat_history"):
                    st.session_state.pop(k, None)
                st.success(f"Deleted {res['meetings']} meeting(s) and {res['audio_files']} audio file(s).")
            except Exception as e:
                st.error(f"Deletion failed: {e}. Please email {SUPPORT_EMAIL}.")
