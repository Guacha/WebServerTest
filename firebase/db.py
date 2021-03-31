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
	print("Inicializando Firebase")
	_ = firebase_admin.initialize_app(CREDS)
	__db = firestore.client()
	print("Firebase Inicializado asíncronamente con éxito")


def gen_game(start_name: str, start_url: str, end_name: str, end_url: str):
	global __db

	created, doc_ref = __db.collection("games").add(
		{"start_name": start_name,
		 "start_url":start_url,
		 "end_name": end_name,
		 "end_url": end_url})
	
	return doc_ref.id
	
	
def get_game(game_id):
	global __db
	game = __db.collection("games").document(game_id).get().to_dict()
	return game

def generate_attempt(gamecode, clicks, timer):
	global __db
	_, attempt = __db.collection("games").document(gamecode).collection("attempts").add({
		"clicks": clicks,
		"name": None,
		"time": timer
	})
	return attempt.id