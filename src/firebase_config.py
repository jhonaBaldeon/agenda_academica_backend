import os
import json
from firebase_admin import credentials, initialize_app, firestore

_firebase_initialized = False
_db = None


def init_firebase():
    global _firebase_initialized, _db

    if _firebase_initialized:
        return firestore.client()

    try:
        # Intentar obtener las credenciales desde variable de entorno
        firebase_config = os.environ.get("FIREBASE_CONFIG")

        if firebase_config:
            # Parsear la configuración desde JSON
            config_dict = json.loads(firebase_config)
            cred = credentials.Certificate(config_dict)
        else:
            # Usar el archivo de credenciales si existe
            cred_path = os.path.join(
                os.path.dirname(__file__), "firebase-credentials.json"
            )
            if os.path.exists(cred_path):
                cred = credentials.Certificate(cred_path)
            else:
                # Intentar usar Application Default Credentials
                cred = credentials.ApplicationDefault()

        initialize_app(cred)
        _db = firestore.client()
        _firebase_initialized = True
        return _db

    except Exception as e:
        print(f"Error initializing Firebase: {e}")
        # Intentar con Application Default Credentials como respaldo
        try:
            cred = credentials.ApplicationDefault()
            initialize_app(cred, project="agenda-academica-13682")
            _db = firestore.client()
            _firebase_initialized = True
            return _db
        except Exception as e2:
            print(f"Error with ADC: {e2}")
            raise


def get_db():
    global _db
    if _db is None:
        _db = init_firebase()
    return _db
