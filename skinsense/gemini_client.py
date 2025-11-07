# skinsense/gemini_client.py
# Requires: pip install google-genai

import os
from google import genai
from google.genai import types


def generate_ai_response(prompt: str):
    """
    Sends a text prompt to the Gemini 2.5 Pro model and returns a structured, user-friendly skincare recommendation.
    """

    # --- Initialize the client ---
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY")
    )

    model = "gemini-2.5-pro"

    # --- SkinSense Gemini System Prompt ---
    system_prompt = (
    "You are SkinSense AI, a professional and friendly dermatology assistant. "
    "The user will provide a skin condition and its risk level (Low, Medium, or High). "
    "Your task is to give **only** structured, evidence-based skincare advice. "
    "Respond directly — do not include greetings, introductions, or phrases like "
    "'Of course, I can help' or 'Sure, here's what I found.' "
    "Start immediately with the headings below.\n\n"
    "=== Response Format ===\n"
    "Condition: <condition name>\n"
    "Risk Level: <Low / Medium / High>\n"
    "Recommendation: <2–4 sentences of actionable advice>\n"
    "References: <at least one trusted medical organization or source>\n\n"
    "=== Guidelines ===\n"
    "1. If Risk = High → Urgently advise visiting a dermatologist, and explain why.\n"
    "2. If Risk = Medium → Recommend seeing a doctor if symptoms worsen; provide practical daily-care and trigger-avoidance advice.\n"
    "3. If Risk = Low → Offer gentle self-care advice like cleansing, hydration, and sun protection.\n"
    "4. Always cite reputable references such as the American Academy of Dermatology (AAD), World Health Organization (WHO), or NHS UK.\n"
    "5. Use a clear, confident tone. No greetings, no small talk, no repetition. "
    "Keep it short — 4–5 sentences max in the Recommendation section."
  )

    # --- Combine system + user input ---
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=f"{system_prompt}\n\nUser input: {prompt}")],
        ),
    ]

    # --- Configure generation ---
    generate_content_config = types.GenerateContentConfig(
        temperature=0.7,  # lower = more focused
        thinking_config=types.ThinkingConfig(thinking_budget=1000),
    )

    # --- Generate content ---
    full_response = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        if hasattr(chunk, "text") and chunk.text:
            full_response += chunk.text

    return full_response.strip()
