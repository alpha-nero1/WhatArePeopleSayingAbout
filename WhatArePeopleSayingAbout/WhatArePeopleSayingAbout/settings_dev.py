# File to override prod settings if ran in dev mode.
from pathlib import Path
import os

DEBUG = True
ENDPOINT_URL = 'http://127.0.0.1:8000/'

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

SECRET_KEY = 'django-insecure-wq*w*+-f*)*-s6oqy5hj1iq(k)ehjp-e)tr3_wy69k01b@v5w&'