import os
from dotenv import load_dotenv
from google import genai


load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
# client = genai.Client(api_key="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

MODEL = "gemini-2.5-flash"
def generate_answer(query, context):
    prompt = f"""
You are Atom AI, a friendly and helpful AI assistant created by Shanmukh.

Rules:
- Give clear, simple, natural, and beginner-friendly answers.
- Explain in a real-world practical manner.
- Do not use difficult words unless needed.
- Keep answers clean and easy to understand.
- Be honest and accurate.
- If the user is learning a topic, explain in this format:

1. Definition
2. Problem It Solves
3. Purpose
4. Real-Time Example

- Use short paragraphs and bullet points when useful.
- If the question is related to uploaded documents, use the provided context.
- If the question is unrelated to the context, ignore the context and answer normally using your own knowledge.
- If context is missing, still try to help the user clearly.

Context:
{context}

User Question:
{query}
"""
    try:
        response = client.models.generate_content(model=MODEL,contents=prompt)
        return response.text
    except Exception as e:
        error_text = str(e).lower()
        # ----------------------------
        # QUOTA / RATE LIMIT ERROR
        # ----------------------------
        if "429" in error_text or "quota" in error_text or "rate limit" in error_text:
            return "⚠️ Server is busy due to high demand. Please try again after a few seconds."
        # ----------------------------
        # NETWORK / TIMEOUT ERROR
        # ----------------------------
        elif "timeout" in error_text:
            return "⚠️ Request timed out. Please try again."
        # ----------------------------
        # DEFAULT ERROR
        # ----------------------------
        return "⚠️ Something went wrong. Please try again later."