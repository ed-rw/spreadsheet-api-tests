"""
Load constants from environment variables here
"""

import os


SERVICE_BASE_URL = os.environ.get("SERVICE_BASE_URL", "http://127.0.0.1:8000")
