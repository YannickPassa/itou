import os

from ._sentry import sentry_init
from .base import *  # noqa: F401,F403


ALLOWED_HOSTS = ["127.0.0.1", "staging.inclusion.beta.gouv.fr", "staging.emplois.inclusion.beta.gouv.fr"]

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "HOST": os.environ.get("POSTGRESQL_ADDON_DIRECT_HOST"),
        "PORT": os.environ.get("POSTGRESQL_ADDON_DIRECT_PORT"),
        "NAME": os.environ.get("POSTGRESQL_ADDON_DB"),
        "USER": os.environ.get("POSTGRESQL_ADDON_CUSTOM_USER"),
        "PASSWORD": os.environ.get("POSTGRESQL_ADDON_CUSTOM_PASSWORD"),
    }
}

ITOU_ENVIRONMENT = "STAGING"
ITOU_PROTOCOL = "https"
ITOU_FQDN = "staging.emplois.inclusion.beta.gouv.fr"
ITOU_EMAIL_CONTACT = "assistance+staging@inclusion.beta.gouv.fr"
DEFAULT_FROM_EMAIL = "noreply+staging@inclusion.beta.gouv.fr"

sentry_init(dsn=os.environ["SENTRY_DSN_STAGING"])

ASP_ITOU_PREFIX = "YYYYY"

FRANCE_CONNECT_BASE_URL = "https://fcp.integ01.dev-franceconnect.fr/api/v1/"
