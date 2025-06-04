"""
Configuration and Settings of the application.

Including env variables.
"""

import os
from dotenv import load_dotenv
from .utils import assert_ret

load_dotenv()

DATABASE_URL = assert_ret(os.getenv("DATABASE_URL"))
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
