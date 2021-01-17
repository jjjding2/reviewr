import os
import secrets

basedir = os.path.abspath(os.path.dirname(__file__))

client_id = os.environ.get("REDDIT_CID")
client_secret = os.environ.get("REDDIT_CSECRET")

# App Settings
SECRET_KEY = secrets.token_hex(16)
WTF_CSRF_ENABLED = False











