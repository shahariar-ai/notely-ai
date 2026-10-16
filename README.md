# Notely AI

**From speech to summary in seconds.** Upload or record a meeting or lecture and get a speaker-labelled
transcript, a summary with action items, study material, and exports you can download.

**Live app:** https://notely-ai-gbbmeelnywb33qddustnay.streamlit.app

## What it does today

- **Transcribe** an uploaded file (mp3 / wav / m4a, up to 500 MB) or a live recording from your browser microphone.
  Speakers are labelled; names are used when they are mentioned in the audio.
- **Summarize:** executive summary, key highlights, action items.
- **Study Mode:** lecture notes, key concepts, flashcards and multiple-choice quizzes.
- **Business Mode:** meeting minutes, executive report, decision log and follow-ups.
- **Translate** summaries (Bengali, English, Spanish, French, German, Arabic, Hindi, Chinese, Japanese).
- **My Meetings:** saved history, natural-language search, and sharing a meeting with another user by email.
- **Ask Notely:** chat with your past meetings.
- **Export** to TXT, DOCX and PDF (the PDF supports Bengali text).
- **Desktop Recorder** (Windows): records your mic and system audio for Zoom / Meet / online classes.
  See [notely-recorder](https://github.com/shahariar-ai/notely-recorder).
- Installable as a PWA.
- Free with daily limits (default 5 transcriptions and 40 other AI actions per user per day).

## Roadmap (not built yet)

Google Calendar integration, live captions, an auto-join meeting bot, and mobile apps.

## Tech

Streamlit · Google Gemini · Supabase (auth, database, storage) · python-docx · fpdf2

## Run locally

```bash
python -m venv venv
venv\Scripts\activate          # macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file (never commit it):

```
GEMINI_API_KEY=...
SUPABASE_URL=...
SUPABASE_KEY=...
# optional
DAILY_TRANSCRIBE_LIMIT=5
DAILY_AI_LIMIT=40
```

Then `streamlit run app.py`. On Streamlit Cloud, put the same keys in the app's *Secrets*
(config reads environment variables first, then `st.secrets`).

### Supabase setup

- A `meetings` table (`user_id`, `title`, `transcript`, `summary_json`, `study_json`, `audio_filename`,
  `shared_with`, `created_at`) and a storage bucket named `audio`.
- Run [`supabase_usage.sql`](supabase_usage.sql) in the SQL editor to enable the per-user daily usage cap.
  Until you do, the app works but does not enforce a cap.

## Privacy

Audio and text are processed by Google Gemini and stored in Supabase. Users can delete their data from
the in-app Privacy page. Contact: shahriar.sharif406@gmail.com

Built by [Shahariar Sharif](https://github.com/shahariar-ai) · powered by FutureTech.ai
