from __future__ import annotations
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.config.settings")
django.setup()
