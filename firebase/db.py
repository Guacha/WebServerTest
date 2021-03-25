import firebase_admin
from firebase_admin import firestore, credentials
from os import environ

ENV_KEYS = {
	"type": "service_account",
	"private_key_id": environ["PRIVATE_ID_KEY"],
	"private_key": environ["PRIVATE_KEY"].replace("\\n", "\n"),
	"client_email": environ["CLIENT_EMAIL"],
	"client_id": environ["CLIENT_ID"],
	"token_uri": environ["TOKEN_URI"],
	"project_id": environ["PROJECT_ID"],
}

CREDS = credentials.Certificate(ENV_KEYS)

__db = None

def init_db_client():
	global __db
	_ = firebase_admin.initialize_app(CREDS)
	__db = firestore.client()
	