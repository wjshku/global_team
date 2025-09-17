import os
import sys

# Ensure the backend directory is on sys.path for imports when running on Vercel
CURRENT_DIR = os.path.dirname(__file__)
BACKEND_DIR = os.path.dirname(CURRENT_DIR)
if BACKEND_DIR not in sys.path:
    sys.path.append(BACKEND_DIR)

# Import FastAPI app from backend/app.py
from app import app as fastapi_app  # type: ignore

# Expose as module-level `app` so Vercel Python runtime can detect ASGI app
app = fastapi_app


