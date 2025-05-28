"""
Configuration and Settings of the application.

Including env variables.
"""

import os
from dotenv import load_dotenv
from .utils import assert_ret

load_dotenv()

DATABASE_URL = assert_ret(os.getenv("DATABASE_URL"))
