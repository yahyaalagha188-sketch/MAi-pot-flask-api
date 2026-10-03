"""
Configuration Module for MAi pot Flask API
"""
import os
from dotenv import load_dotenv

load_dotenv()

# App Configuration
APP_NAME = "MAi pot"
DEVELOPER_NAME = "Yahya.Kurdistan"
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
PORT = int(os.getenv("PORT", "5000"))

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Deployment
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL", "")
KEEP_ALIVE_INTERVAL = int(os.getenv("KEEP_ALIVE_INTERVAL", "300"))

# Rate Limiting
RATE_LIMIT_ENABLED = os.getenv("RATE_LIMIT_ENABLED", "True").lower() == "true"
RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
RATE_LIMIT_PERIOD = int(os.getenv("RATE_LIMIT_PERIOD", "3600"))

# Models & Response
OPENAI_MODEL = "gpt-4o"
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1500"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "app.log")

# CORS
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
