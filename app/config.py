import os
import ldap

from django_auth_ldap.config import LDAPSearch

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

DEBUG = os.getenv("DJANGO_DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = os.getenv(
    "DJANGO_ALLOWED_HOSTS",
    "localhost,127.0.0.1"
).split(",")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["/app/templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "/data/db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
]

LANGUAGE_CODE = "fr-fr"

TIME_ZONE = "Europe/Paris"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

STATIC_ROOT = "/app/staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = "/login/"

LOGIN_REDIRECT_URL = "/"

LOGOUT_REDIRECT_URL = "/login/"

# -------------------------------------------------
# AUTHENTIFICATION ACTIVE DIRECTORY / LDAP
# -------------------------------------------------

AUTHENTICATION_BACKENDS = [
    "django_auth_ldap.backend.LDAPBackend",
    "django.contrib.auth.backends.ModelBackend",
]

AUTH_LDAP_SERVER_URI = os.environ["LDAP_SERVER_URI"]

AUTH_LDAP_BIND_DN = os.environ["LDAP_BIND_DN"]

AUTH_LDAP_BIND_PASSWORD = os.environ["LDAP_BIND_PASSWORD"]

# Recherche de l'utilisateur dans Active Directory

AUTH_LDAP_USER_SEARCH = LDAPSearch(
    os.environ["LDAP_USER_BASE_DN"],
    ldap.SCOPE_SUBTREE,
    "(sAMAccountName=%(user)s)"
)

# Correspondance des attributs AD / Django

AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail",
}

# Création automatique des utilisateurs Django
# lors de leur première authentification LDAP.

AUTH_LDAP_ALWAYS_UPDATE_USER = True

# Désactivation des referrals AD non nécessaires
# dans cette configuration de laboratoire.

AUTH_LDAP_CONNECTION_OPTIONS = {
    ldap.OPT_REFERRALS: 0,
}

# LDAP avec StartTLS.
# À utiliser avec un certificat serveur valide et
# une autorité de certification reconnue.

AUTH_LDAP_START_TLS = (
    os.getenv("LDAP_START_TLS", "True").lower() == "true"
)

# Ne pas accepter les certificats LDAP invalides.
ldap.set_option(ldap.OPT_X_TLS_CACERTFILE, "/certs/ca.pem")
ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_DEMAND)

# -------------------------------------------------
# SESSIONS ET SECURITE
# -------------------------------------------------

SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = (
    os.getenv("COOKIE_SECURE", "False").lower() == "true"
)
CSRF_COOKIE_SECURE = SESSION_COOKIE_SECURE

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
