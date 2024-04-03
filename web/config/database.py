import logging

import dj_database_url

from .env import ENV

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

_default_db_url = "sqlite:///db.sqlite3"
DB_URL = ENV.str("POSTGRES_URL", _default_db_url)
if _default_db_url == DB_URL:
    logging.warning(f"Using default database url: '{DB_URL}'", )

CONN_MAX_AGE = ENV.int("CONN_MAX_AGE", 600)

DATABASES = {
    "default": dj_database_url.parse(
        DB_URL,
        conn_max_age=CONN_MAX_AGE),
}
