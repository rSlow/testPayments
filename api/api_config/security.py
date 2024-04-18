import logging

from .base import ENV

_default_secret_key = "your-super-secret-and-long-django-secret-key"  # noqa: S105
SECRET_KEY = ENV.str("DJANGO_SECRET_KEY", _default_secret_key)
if _default_secret_key == SECRET_KEY:
    logging.warning("You are using a default Django secret key")

DEBUG = ENV.bool("DJANGO_DEBUG", False)

ALLOWED_HOSTS: list[str] = ENV.list("ALLOWED_HOSTS", ["127.0.0.1", "localhost"])
ALLOWED_HOSTS.extend(["localhost", "127.0.0.1"])

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

CSRF_TRUSTED_ORIGINS: list[str] = ENV.list("CSRF_TRUSTED_ORIGINS", ["http://localhost"])
CSRF_TRUSTED_ORIGINS.extend(["http://localhost", "http://127.0.0.1"])

CORS_ALLOW_ALL_ORIGINS = ENV.bool("CORS_ALLOW_ALL_ORIGINS", False)
CORS_ALLOW_CREDENTIALS = ENV.bool("CORS_ALLOW_CREDENTIALS", False)
CORS_ALLOWED_ORIGINS = ENV.list("CORS_ALLOWED_ORIGINS", ["http://localhost"])
