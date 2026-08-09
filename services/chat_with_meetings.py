import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL

genai.configure(api_key=GEMINI_API_KEY)


def chat_with_meetings(question: str, meetings: list, chat_history: list) -> str:
    """
    RAG-style chat: feed all meeting summaries+transcripts (trimmed) as context,
    plus the running chat history, then answer the question.
    """
    context_blocks = []
    for m in meetings:
        summary = (m.get("summary_json") or {}).get("executive_summary", "")
        transcript_snippet = (m.get("transcript") or "")[:1500]
        context_blocks.append(
            f"--- Meeting: {m.get('title')} ({m.get('created_at', '')[:10]}) ---\n"
            f"Summary: {summary}\n"
            f"Transcript excerpt: {transcript_snippet}"
        )
    context = "\n\n".join(context_blocks) if context_blocks else "No meetings yet."

    history_text = "\n".join(
        f"{'User' if h['role'] == 'user' else 'Assistant'}: {h['content']}"
        for h in chat_history[-6:]
    )

    prompt = f"""You are Notely AI's assistant. Answer the user's question using ONLY
the meeting context below. If the answer isn't in the context, say so clearly.
Cite which meeting(s) you're drawing from by title.

MEETING CONTEXT:
{context}

RECENT CONVERSATION:
{history_text}

User question: {question}
"""
    model = genai.GenerativeModel(GEMINI_MODEL)
    response = model.generate_content(prompt)
    return response.text.strip()