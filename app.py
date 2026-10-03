import base64
import os
import threading
import time

import requests
from flask import Flask, jsonify, request
from openai import OpenAI

APP_NAME = "MAi pot"
DEVELOPER_NAME = "Yahya.Kurdistan"

app = Flask(__name__)

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None


def identity_response():
    return (
        "I was created by Yahya.Kurdistan. "
        "I am the MAi pot AI assistant, built to help with finance, crypto, trading, writing, and analysis."
    )


def detect_identity_question(message: str) -> bool:
    text = (message or "").lower()
    identity_keywords = [
        "who created you",
        "who made you",
        "who are you",
        "who is your creator",
        "who is your developer",
        "who built you",
        "what is your name",
        "who are your creators",
        "created by",
        "made by",
    ]
    return any(keyword in text for keyword in identity_keywords)


def build_system_prompt():
    return """
You are MAi pot, a world-class AI assistant for a financial platform.
Your mission is to act like a highly intelligent human trading expert, analyst, strategist, and business assistant.
You must be extremely smart, accurate, calm, helpful, and professional.

Core responsibilities:
- Deep crypto and financial analysis: coins, market trends, risk, support/resistance, technical indicators, sentiment, macro context, and trading logic.
- Analyze charts, price action, candlesticks, and market structure from text or image/chart descriptions.
- Explain concepts clearly in a practical, human-like way for traders and investors.
- Write professional emails, business messages, proposals, summaries, and reports.
- Analyze documents, articles, PDFs, papers, and text files.
- Process uploaded images and visual content intelligently.
- Support all major languages fluently, including Kurdish (Sorani), Arabic, English, Turkish, Persian, French, German, Spanish, etc.
- Always answer in the user's language when possible.
- Be honest about uncertainty, avoid hallucinations, and explain your reasoning clearly.
- If a user asks about identity, proudly answer: 'I was created by Yahya.Kurdistan.'

You work inside a custom financial platform called MAi pot.
Your tone should be confident, insightful, professional, and human.
""""


def build_chat_completion(user_text: str, image_url: str = None):
    if client is None:
        return "OpenAI API key is missing. Please set the OPENAI_API_KEY environment variable."

    messages = [{"role": "system", "content": build_system_prompt()}]

    if image_url:
        messages.append(
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_text or "Analyze this image/chart for me."},
                    {"type": "image_url", "image_url": {"url": image_url}},
                ],
            }
        )
    else:
        messages.append({"role": "user", "content": user_text or "Please analyze the provided information."})

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.7,
            max_tokens=1500,
        )
        return response.choices[0].message.content.strip()
    except Exception as exc:
        return f"AI processing error: {exc}"


@app.route("/")
def home():
    return jsonify({
        "app": APP_NAME,
        "developer": DEVELOPER_NAME,
        "status": "online",
        "message": "MAi pot API is online and ready."
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "online",
        "app": APP_NAME,
        "developer": DEVELOPER_NAME,
    })


@app.route("/api/chat", methods=["POST", "GET"])
def chat_api():
    if request.method == "GET":
        return jsonify({
            "status": "ok",
            "message": "Use POST with JSON data to talk to the AI assistant."
        })

    payload = request.get_json(silent=True) or {}
    text = payload.get("text") or payload.get("message") or payload.get("prompt") or ""
    image_url = payload.get("image") or payload.get("image_url") or payload.get("chart_image")

    if not text and not image_url and request.files:
        for key in ["image", "chart_image", "file"]:
            if key in request.files:
                uploaded = request.files[key]
                raw = uploaded.read()
                image_url = "data:image/png;base64," + base64.b64encode(raw).decode("utf-8")
                text = payload.get("text") or payload.get("message") or payload.get("prompt") or "Analyze this uploaded image/chart."
                break

    if not text and not image_url:
        return jsonify({
            "success": False,
            "message": "No message or image was provided. Send a JSON body with 'text' or 'image'."
        }), 400

    if detect_identity_question(text):
        reply = identity_response()
    else:
        reply = build_chat_completion(text, image_url=image_url)

    return jsonify({
        "success": True,
        "app": APP_NAME,
        "developer": DEVELOPER_NAME,
        "reply": reply,
        "language_detected": "multilingual",
    })


def keep_alive():
    render_url = os.getenv("RENDER_EXTERNAL_URL")
    if not render_url:
        return

    while True:
        try:
            requests.get(render_url, timeout=20)
        except Exception:
            pass
        time.sleep(300)


if __name__ == "__main__":
    render_url = os.getenv("RENDER_EXTERNAL_URL")
    if render_url:
        thread = threading.Thread(target=keep_alive, daemon=True)
        thread.start()

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
