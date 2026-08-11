import os
import streamlit as st
from streamlit_mic_recorder import mic_recorder

from config import AUDIO_DIR, EXPORT_DIR
from services.transcription import transcribe_audio
from services.summarizer import summarize_transcript
from services.study_mode import generate_study_pack
from services.business_mode import generate_business_pack
from services.translator import translate_text
from services.ai_search import ai_search
from services.exporter import export_txt, export_docx, export_pdf
from services.storage import save_meeting, get_all_meetings, search_meetings
from services.auth import sign_up, sign_in, sign_out
from services.chat_with_meetings import chat_with_meetings
from services.collaboration import share_meeting, unshare_meeting, get_shared_with_me
from services.calendar_service import get_upcoming_events
from utils.audio_utils import save_uploaded_file, save_recorded_audio, upload_audio_to_cloud

os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(EXPORT_DIR, exist_ok=True)

st.set_page_config(page_title="Notely AI", page_icon="🎙️", layout="wide")

# ---------- PWA tags ----------
st.markdown(
    """
    <link rel="manifest" href="app/static/manifest.json">
    <meta name="theme-color" content="#6366f1">
    <link rel="apple-touch-icon" href="app/static/icon-192.png">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="Notely AI">
    <script>
      if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('app/static/service-worker.js')
          .then(() => console.log('Notely AI service worker registered'))
          .catch((err) => console.log('SW registration failed', err));
      }
    </script>
    """,
    unsafe_allow_html=True,
)

# ---------- Premium styling ----------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&family=Inter:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: linear-gradient(180deg, #0b0d17 0%, #10131f 100%);
    }

    h1 {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 700 !important;
        background: linear-gradient(90deg, #818cf8, #c084fc, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.5px;
    }

    h2, h3 {
        font-family: 'Poppins', sans-serif !important;
        color: #e5e7eb !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background-color: rgba(255,255,255,0.03);
        padding: 6px;
        border-radius: 14px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 8px 16px;
        color: #9ca3af;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #6366f1, #8b5cf6);
        color: white !important;
    }

    .stButton > button {
        border-radius: 10px;
        border: 1px solid rgba(129,140,248,0.4);
        background: linear-gradient(90deg, #6366f1, #8b5cf6);
        color: white;
        font-weight: 600;
        padding: 0.5rem 1.2rem;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(139,92,246,0.35);
        border-color: rgba(139,92,246,0.6);
    }

    .stTextInput input, .stSelectbox div[data-baseweb="select"] {
        border-radius: 10px !important;
        background-color: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
    }

    .streamlit-expanderHeader {
        background-color: rgba(255,255,255,0.03);
        border-radius: 10px;
        font-weight: 500;
    }

    .stAlert {
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.06);
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f1119, #151827);
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "user" not in st.session_state:
    st.session_state.user = None

# ---------- LOGIN GATE ----------
if st.session_state.user is None:
    st.markdown(
        """
        <div style="text-align:center; padding: 2rem 0 1rem 0;">
            <h1 style="font-size: 2.6rem; margin-bottom:0;">Notely AI</h1>
            <p style="color:#9ca3af; font-size:1.05rem; margin-top:0.2rem;">
                From Speech to Summary in Seconds
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    login_tab, signup_tab = st.tabs(["Login", "Sign Up"])
    with login_tab:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pw")
        if st.button("Login"):
            try:
                result = sign_in(email, password)
                st.session_state.user = result.user
                st.rerun()
            except Exception as e:
                st.error(f"Login failed: {e}")
    with signup_tab:
        email2 = st.text_input("Email", key="signup_email")
        password2 = st.text_input("Password", type="password", key="signup_pw")
        if st.button("Create Account"):
            try:
                sign_up(email2, password2)
                st.success("Account created! You can now log in.")
            except Exception as e:
                st.error(f"Signup failed: {e}")
    st.stop()

# ---------- MAIN APP ----------
user_id = st.session_state.user.id
st.sidebar.write(f"Logged in as: {st.session_state.user.email}")
if st.sidebar.button("Log out"):
    sign_out()
    st.session_state.user = None
    st.rerun()

st.markdown(
    """
    <div style="text-align:center; padding: 1.5rem 0 0.5rem 0;">
        <h1 style="font-size: 2.6rem; margin-bottom:0;">Notely AI</h1>
        <p style="color:#9ca3af; font-size:1.05rem; margin-top:0.2rem;">
            From Speech to Summary in Seconds — powered by FutureTech.ai
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
    [
        "🎤 New Recording", "📚 Study Mode", "💼 Business Mode", "🌐 Translate",
        "🗂️ My Meetings", "💬 Ask Notely", "📅 Calendar",
    ]
)

for key, default in [("last_transcript", None), ("last_summary", None), ("last_title", "")]:
    if key not in st.session_state:
        st.session_state[key] = default

with tab1:
    title = st.text_input("Meeting / Lecture title", value="Untitled Meeting")
    st.subheader("Option A: Upload an audio file")
    uploaded_file = st.file_uploader("Upload mp3 / wav / m4a", type=["mp3", "wav", "m4a"])
    st.subheader("Option B: Record live")
    audio = mic_recorder(start_prompt="🔴 Start Recording", stop_prompt="⏹️ Stop", key="recorder")

    audio_path = None
    if uploaded_file is not None:
        audio_path = save_uploaded_file(uploaded_file)
    elif audio is not None:
        audio_path = save_recorded_audio(audio["bytes"], f"{title.replace(' ', '_')}.wav")
        st.audio(audio["bytes"])

    if audio_path and st.button("🚀 Transcribe & Summarize"):
        with st.spinner("Transcribing with Gemini..."):
            transcript = transcribe_audio(audio_path)
        with st.spinner("Generating summary..."):
            summary = summarize_transcript(transcript)
        with st.spinner("Uploading audio to cloud..."):
            try:
                audio_url = upload_audio_to_cloud(audio_path, user_id)
            except Exception as e:
                audio_url = None
                st.warning(f"Cloud audio upload skipped: {e}")

        st.session_state.last_transcript = transcript
        st.session_state.last_summary = summary
        st.session_state.last_title = title

        save_meeting(user_id, title, transcript, summary, None, audio_url)
        st.success("Done! Saved to cloud.")

        st.subheader("Executive Summary")
        st.write(summary.get("executive_summary", ""))
        st.subheader("Key Highlights")
        for h in summary.get("key_highlights", []):
            st.markdown(f"- {h}")
        st.subheader("Action Items")
        for item in summary.get("action_items", []):
            st.markdown(f"- **{item.get('task')}** — Owner: {item.get('owner')}")
        with st.expander("Full Transcript"):
            st.write(transcript)

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Export as TXT"):
                st.success(f"Saved: {export_txt(title, transcript, summary)}")
        with col2:
            if st.button("Export as DOCX"):
                st.success(f"Saved: {export_docx(title, transcript, summary)}")
        with col3:
            if st.button("Export as PDF"):
                st.success(f"Saved: {export_pdf(title, transcript, summary)}")

with tab2:
    st.subheader("Study Mode")
    if not st.session_state.last_transcript:
        st.info("Transcribe a lecture in the 'New Recording' tab first.")
    else:
        if st.button("Generate Study Pack"):
            with st.spinner("Generating notes, flashcards & MCQs..."):
                st.session_state.last_study = generate_study_pack(st.session_state.last_transcript)
        if "last_study" in st.session_state:
            study = st.session_state.last_study
            st.markdown("### Lecture Notes")
            st.write(study.get("lecture_notes", ""))
            st.markdown("### Key Concepts")
            for c in study.get("key_concepts", []):
                st.markdown(f"- {c}")
            st.markdown("### Flashcards")
            for fc in study.get("flashcards", []):
                with st.expander(fc.get("question", "")):
                    st.write(fc.get("answer", ""))
            st.markdown("### MCQs")
            for i, mcq in enumerate(study.get("mcqs", [])):
                st.markdown(f"**Q{i+1}: {mcq.get('question')}**")
                choice = st.radio("Choose:", mcq.get("options", []), key=f"mcq_{i}")
                if st.button(f"Check Q{i+1}", key=f"check_{i}"):
                    if choice == mcq.get("correct_answer"):
                        st.success("Correct!")
                    else:
                        st.error(f"Incorrect. Correct answer: {mcq.get('correct_answer')}")

with tab3:
    st.subheader("Business Mode")
    if not st.session_state.last_transcript:
        st.info("Transcribe a meeting in the 'New Recording' tab first.")
    else:
        if st.button("Generate Business Pack"):
            with st.spinner("Generating MoM, report & action plan..."):
                st.session_state.last_business = generate_business_pack(st.session_state.last_transcript)
        if "last_business" in st.session_state:
            biz = st.session_state.last_business
            st.markdown("### Meeting Minutes (MoM)")
            st.write(biz.get("meeting_minutes", ""))
            st.markdown("### Executive Report")
            st.write(biz.get("executive_report", ""))
            st.markdown("### Decision Log")
            for d in biz.get("decision_log", []):
                st.markdown(f"- **{d.get('decision')}** — {d.get('context')}")
            st.markdown("### Follow-ups")
            for f in biz.get("follow_ups", []):
                st.markdown(f"- {f.get('task')} — Owner: {f.get('owner')}, Due: {f.get('due')}")

with tab4:
    st.subheader("Translate")
    if not st.session_state.last_summary:
        st.info("Transcribe a session in the 'New Recording' tab first.")
    else:
        lang = st.selectbox(
            "Target language",
            ["Bengali", "English", "Spanish", "French", "German", "Arabic", "Hindi", "Chinese", "Japanese"],
        )
        if st.button("Translate Summary"):
            with st.spinner("Translating..."):
                translated = translate_text(
                    st.session_state.last_summary.get("executive_summary", ""), lang
                )
            st.write(translated)

with tab5:
    sub1, sub2 = st.tabs(["My Meetings", "Shared With Me"])

    with sub1:
        query = st.text_input("🔍 Search meetings (natural language)")
        all_meetings = get_all_meetings(user_id)
        meetings = ai_search(query, all_meetings) if query else all_meetings

        for m in meetings:
            with st.expander(f"{m['title']} — {m['created_at'][:16]}"):
                st.write((m["transcript"] or "")[:500] + "...")
                if m.get("audio_filename"):
                    st.audio(m["audio_filename"])

                share_email = st.text_input("Share with (email)", key=f"share_{m['id']}")
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("Share", key=f"share_btn_{m['id']}"):
                        share_meeting(m["id"], user_id, share_email)
                        st.success(f"Shared with {share_email}")
                with col_b:
                    if st.button("Unshare", key=f"unshare_btn_{m['id']}"):
                        unshare_meeting(m["id"], user_id, share_email)
                        st.success(f"Removed {share_email}")

                if m.get("shared_with"):
                    st.caption(f"Shared with: {', '.join(m['shared_with'])}")

    with sub2:
        shared = get_shared_with_me(st.session_state.user.email)
        if not shared:
            st.info("No one has shared anything with you yet.")
        for m in shared:
            with st.expander(f"{m['title']} — {m['created_at'][:16]}"):
                st.write((m["transcript"] or "")[:500] + "...")

with tab6:
    st.subheader("💬 Ask Notely — ask about your past meetings")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    question = st.chat_input("e.g. What decisions came out of last week's budget meeting?")
    if question:
        st.session_state.chat_history.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)

        with st.spinner("Searching your meetings..."):
            all_meetings = get_all_meetings(user_id)
            answer = chat_with_meetings(question, all_meetings, st.session_state.chat_history)

        st.session_state.chat_history.append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.write(answer)

with tab7:
    st.subheader("📅 Upcoming Calendar Events")
    if st.button("Connect / Refresh Google Calendar"):
        try:
            with st.spinner("Connecting to Google Calendar... (a browser login may open)"):
                st.session_state.calendar_events = get_upcoming_events()
        except Exception as e:
            st.error(f"Calendar connect failed: {e}")

    if "calendar_events" in st.session_state:
        for ev in st.session_state.calendar_events:
            with st.container(border=True):
                st.markdown(f"**{ev['title']}**")
                st.caption(ev["start"])
                if ev["meeting_link"]:
                    st.markdown(f"[Join Meeting]({ev['meeting_link']})")

# ---------- Desktop Recorder download ----------
st.markdown("---")
with st.expander("🖥️ Recording a Zoom / Google Meet / online class? Download the Desktop Recorder"):
    st.write(
        "Notely AI's browser mic only captures your own voice. To record an "
        "online meeting or class (everyone's audio), download our free "
        "desktop companion app, click Start before your meeting, and Stop "
        "after — then upload the file here."
    )
    st.markdown(
        "[⬇️ Download Notely Recorder for Windows](https://github.com/shahariar-ai/notely-recorder/releases/download/v1.1.0/NotelyRecorder.exe)"
    )