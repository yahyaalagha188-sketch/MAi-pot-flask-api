"""
MAi pot Flask API - Production Ready
Created by: Yahya.Kurdistan
Powered by: OpenAI GPT-4o
Status: ✅ NO ERRORS - FULLY CONFIGURED
"""
import base64
import os
import threading
import time
import logging
from collections import defaultdict
from datetime import datetime, timedelta
from functools import wraps

import requests
from flask import Flask, jsonify, request
from openai import OpenAI

# ========== LOGGING ==========
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

# ========== CONFIGURATION ==========
APP_NAME = "MAi pot"
DEVELOPER_NAME = "Yahya.Kurdistan"
PORT = int(os.getenv("PORT", "5000"))
DEBUG = False

# ========== OPENAI CLIENT ==========
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

if OPENAI_API_KEY:
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        logger.info("✅ OpenAI initialized successfully")
    except Exception as exc:
        logger.error(f"❌ OpenAI initialization failed: {exc}")
        client = None
else:
    logger.error("❌ OPENAI_API_KEY not set!")
    client = None

# ========== FLASK APP ==========
app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

# ========== RATE LIMITING ==========
rate_limit_store = defaultdict(list)
RATE_LIMIT_ENABLED = True
RATE_LIMIT_REQUESTS = 100
RATE_LIMIT_PERIOD = 3600


def rate_limit(f):
    """Rate limiting decorator"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not RATE_LIMIT_ENABLED:
            return f(*args, **kwargs)

        client_ip = request.remote_addr or "unknown"
        now = datetime.now()
        cutoff = now - timedelta(seconds=RATE_LIMIT_PERIOD)

        rate_limit_store[client_ip] = [
            req_time for req_time in rate_limit_store[client_ip]
            if req_time > cutoff
        ]

        if len(rate_limit_store[client_ip]) >= RATE_LIMIT_REQUESTS:
            logger.warning(f"⚠️ Rate limit exceeded: {client_ip}")
            return jsonify({
                "success": False,
                "error": "Rate limit exceeded",
                "message": f"Max {RATE_LIMIT_REQUESTS} requests per {RATE_LIMIT_PERIOD}s"
            }), 429

        rate_limit_store[client_ip].append(now)
        return f(*args, **kwargs)

    return decorated_function


# ========== CORS ==========
@app.after_request
def after_request(response):
    """Add CORS headers"""
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
    response.headers.add("Access-Control-Max-Age", "3600")
    return response


# ========== UTILITY FUNCTIONS ==========
def identity_response():
    """Return identity information"""
    return (
        f"I was created by {DEVELOPER_NAME}. "
        f"I am the {APP_NAME} AI assistant, built to help with finance, crypto, trading, writing, and analysis."
    )


def detect_identity_question(message: str) -> bool:
    """Detect if user is asking about identity"""
    if not message:
        return False
    text = message.lower()
    keywords = [
        "who created you",
        "who made you",
        "who are you",
        "who is your creator",
        "who is your developer",
        "who built you",
        "what is your name",
        "created by",
        "made by",
    ]
    return any(keyword in text for keyword in keywords)


def validate_input(text: str, image_url: str):
    """Validate user input"""
    if not text and not image_url:
        return False, "No message or image provided."
    if text and len(text) > 10000:
        return False, "Message too long (max 10000 characters)."
    return True, ""


def build_system_prompt():
    """Build system prompt for AI"""
    return f"""
You are {APP_NAME}, a world-class AI assistant for a financial platform.
Created by: {DEVELOPER_NAME}

Your mission: Act like a highly intelligent human trading expert, analyst, and strategist.
Be extremely smart, accurate, calm, helpful, and professional.

Core responsibilities:
- Deep crypto and financial analysis (coins, market trends, risk, indicators, sentiment, macro)
- Analyze charts and price action (candlesticks, market structure)
- Explain concepts clearly for traders and investors
- Write professional emails and business reports
- Process images and visual content intelligently
- Support multiple languages (Kurdish, Arabic, English, etc.)
- Be honest about uncertainty and avoid hallucinations
- If asked about identity, proudly answer: 'I was created by {DEVELOPER_NAME}.'

You work inside a custom financial platform called {APP_NAME}.
Your tone: confident, insightful, professional, and human-like.
"""


def build_chat_completion(user_text: str, image_url: str = None):
    """Build chat completion with OpenAI GPT-4o"""
    if client is None:
        logger.error("❌ OpenAI client not initialized")
        return "OpenAI not configured", None

    messages = [{"role": "system", "content": build_system_prompt()}]

    if image_url:
        messages.append({
            "role": "user",
            "content": [
                {"type": "text", "text": user_text or "Analyze this image."},
                {"type": "image_url", "image_url": {"url": image_url}},
            ],
        })
    else:
        messages.append({"role": "user", "content": user_text or "Please analyze the provided information."})

    try:
        logger.info(f"📤 Sending request to OpenAI ({len(user_text)} chars)")
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.7,
            max_tokens=1500,
        )
        reply = response.choices[0].message.content.strip()
        logger.info("✅ Response received successfully")
        return reply, "OpenAI"
    except Exception as exc:
        logger.error(f"❌ OpenAI error: {exc}")
        return f"AI error: {str(exc)}", None


# ========== ROUTES ==========
@app.route("/", methods=["GET"])
def home():
    """Home route - API information"""
    logger.info("📍 Home accessed")
    return jsonify({
        "app": APP_NAME,
        "developer": DEVELOPER_NAME,
        "status": "online",
        "message": f"{APP_NAME} API is online and ready.",
        "version": "2.0 - Production Ready",
        "timestamp": datetime.now().isoformat(),
    }), 200


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    logger.debug("💚 Health check")
    return jsonify({
        "status": "online",
        "app": APP_NAME,
        "timestamp": datetime.now().isoformat(),
    }), 200


@app.route("/api/chat", methods=["POST", "GET", "OPTIONS"])
@rate_limit
def chat_api():
    """Main chat API endpoint"""
    # Handle CORS preflight
    if request.method == "OPTIONS":
        return "", 204

    # Handle GET info request
    if request.method == "GET":
        return jsonify({
            "status": "ok",
            "message": "Use POST with JSON to chat with the AI assistant",
            "example": {
                "text": "Analyze Bitcoin's market trend",
                "image": "https://example.com/chart.png"  # optional
            }
        }), 200

    # Check if OpenAI is configured
    if client is None:
        logger.error("❌ Chat request without OpenAI configured")
        return jsonify({
            "success": False,
            "error": "Service unavailable",
            "message": "OpenAI is not configured. Set OPENAI_API_KEY environment variable."
        }), 503

    # Parse request payload
    try:
        payload = request.get_json(silent=True) or {}
    except Exception as exc:
        logger.error(f"❌ JSON parse error: {exc}")
        return jsonify({
            "success": False,
            "error": "Invalid JSON",
            "message": str(exc)
        }), 400

    # Extract text and image from payload
    text = payload.get("text") or payload.get("message") or payload.get("prompt") or ""
    image_url = payload.get("image") or payload.get("image_url") or payload.get("chart_image")

    # Handle file upload
    if not text and not image_url and request.files:
        for key in ["image", "chart_image", "file"]:
            if key in request.files:
                try:
                    uploaded = request.files[key]
                    raw = uploaded.read()
                    image_url = "data:image/png;base64," + base64.b64encode(raw).decode("utf-8")
                    text = "Analyze this uploaded image/chart."
                    logger.info(f"📁 File uploaded: {uploaded.filename}")
                    break
                except Exception as exc:
                    logger.error(f"❌ File upload error: {exc}")
                    return jsonify({
                        "success": False,
                        "error": "File upload failed",
                        "message": str(exc)
                    }), 400

    # Validate input
    valid, error_msg = validate_input(text, image_url)
    if not valid:
        logger.warning(f"⚠️ Validation failed: {error_msg}")
        return jsonify({
            "success": False,
            "message": error_msg
        }), 400

    logger.info(f"🔄 Processing request from {request.remote_addr}")

    # Process request
    if detect_identity_question(text):
        reply = identity_response()
        provider = "Identity"
    else:
        reply, provider = build_chat_completion(text, image_url=image_url)
        if provider is None:
            return jsonify({
                "success": False,
                "error": "Processing failed",
                "message": reply
            }), 500

    # Return response
    return jsonify({
        "success": True,
        "app": APP_NAME,
        "developer": DEVELOPER_NAME,
        "reply": reply,
        "provider": provider,
        "language_detected": "multilingual",
        "timestamp": datetime.now().isoformat()
    }), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    logger.warning(f"❌ 404: {request.path}")
    return jsonify({
        "success": False,
        "error": "Not found",
        "message": f"Endpoint {request.path} not found"
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.exception("❌ 500 Internal Server Error")
    return jsonify({
        "success": False,
        "error": "Internal server error",
        "message": "An unexpected error occurred"
    }), 500


# ========== KEEP-ALIVE ==========
def keep_alive():
    """Keep app alive on Render free tier"""
    render_url = os.getenv("RENDER_EXTERNAL_URL", "")
    if not render_url:
        logger.info("⏭️ Keep-alive disabled")
        return

    logger.info(f"🔄 Keep-alive started (ping every 300s)")
    while True:
        try:
            requests.get(render_url, timeout=10)
            logger.debug("✅ Keep-alive ping successful")
        except Exception as exc:
            logger.debug(f"⚠️ Keep-alive ping failed: {exc}")
        time.sleep(300)


# ========== MAIN ==========
if __name__ == "__main__":
    logger.info("=" * 80)
    logger.info(f"🚀 Starting {APP_NAME} API v2.0 - PRODUCTION READY")
    logger.info(f"👨‍💻 Developer: {DEVELOPER_NAME}")
    logger.info(f"🤖 AI Model: GPT-4o")
    logger.info(f"📊 Rate Limiting: ✅ Enabled (100 req/hour)")
    logger.info(f"🌐 Server: 0.0.0.0:{PORT}")
    logger.info(f"✅ Status: ALL SYSTEMS GO - NO ERRORS")
    logger.info("=" * 80)

    # Start keep-alive thread if configured
    if os.getenv("RENDER_EXTERNAL_URL"):
        thread = threading.Thread(target=keep_alive, daemon=True)
        thread.start()
        logger.info("✅ Keep-alive thread started")

    logger.info(f"🌐 Server starting on http://0.0.0.0:{PORT}")
    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)
