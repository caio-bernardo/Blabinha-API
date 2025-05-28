"""models.py

Expose models from all modules.
"""

from blabinha_api.chats.models import Chat
from blabinha_api.dialogs.models import Dialog

__all__ = ["Chat", "Dialog"]
