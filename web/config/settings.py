from __future__ import annotations

from split_settings.tools import include

include(
    "base.py",
    "security.py",
    "application.py",
    "database.py",
    "auth.py",
    "static.py",
    "logging.py"
)
