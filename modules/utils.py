import streamlit as st
import hashlib
import json
import urllib.request

# 1. VARIABLES GLOBALES DE L'AMICALE BOULE SAINT-GENIX AOSTE
NOM_CLUB = "Amicale Boule Saint-Genix Aoste"
STATUT_CLUB = "Association déclarée (fondée en décembre 2004)"
ADRESSE_SIEGE = "Café Gojon, Rue des Juifs, 73240 Saint-Genix-les-Villages"
BOULODROMES = "Jeux de La Glière (Saint-Genix) & Terrains d'Aoste"
URL_FACEBOOK = "https://facebook.com"

DONNEES_CARTE = {
    "latitude": (45.5995592, 45.590435),
    "longitude": (5.6297572, 5.606534),
    "Nom du terrain": ("Jeux de La Glière (Saint-Genix)", "Terrains de boules d'Aoste")
}

URL_BOULE_IMAGE = "https://taboulot.fr"


# 2. CLIENT WEB REST COMPLET ET SÉCURISÉ (ZÉRO gRPC)
class DocumentSimule:
    def __init__(self, data, exists=True):
        self._data = data
        self.exists = exists
    def to_dict(self):
        return self._data
    def get(self):
        return self

class DocumentRefSimule:
    def __init__(self, project_id, collection_name, doc_id):
        self.project_id = project_id
        self.collection_name = collection_name
        self.doc_id = doc_id
        self.url = f"https://googleapis.com{self.project_id}/databases/(default)/documents/{self.collection_name}/{self.doc_id}"

    def get(self, timeout=None):
        try:
            req = urllib.request.Request(self.url, method="GET")
            with urllib.request.urlopen(req, timeout=4) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                fields = res_data.get("fields", {})
                data_nettoyee = {}
                for key, val in fields.items():
                    if "stringValue" in val:
                        data_nettoyee[key] = val["stringValue"]
                    elif "integerValue" in val:
                        data_nettoyee[key] = int(val["integerValue"])
                    elif "booleanValue" in val:
                        data_nettoyee[key] = val["booleanValue"]
                return DocumentSimule(data_nettoyee, exists=True)
        except Exception:
            return DocumentSimule({}, exists=False)

    def set(self, data):
        fields = {}
        for key, val in data.items():
            if isinstance(val, bool):
                fields[key] = {"booleanValue": val}
            elif isinstance(val, int):
                fields[key] = {"integerValue": str(val)}
            else:
                fields[key] = {"stringValue": str(val)}
        
        payload = {"fields": fields}
        encoded_data = json.dumps(payload).encode("utf-8")
        url_write = f"https://googleapis.com{self.project_id}/databases/(default)/documents/{self.collection_name}?documentId={self.doc_id}"
        try:
            req = urllib.request.Request(url_write, data=encoded_data, method="POST")
            req.add_header("Content-Type", "application/json")
            with urllib.request.urlopen(req, timeout=4) as response:
                return True
        except Exception as e:
            st.error(f"❌ Erreur d'écriture dans la base : {e}")
            return False

class CollectionSimulee:
    def __init__(self, project_id, collection_name):
        self.project_id = project_id
        self.collection_name = collection_name

    def document(self, doc_id):
        return DocumentRefSimule(self.project_id, self.collection_name, doc_id)

    def get(self, timeout=None):
        url = f"https://googleapis.com{self.project_id}/databases/(default)/documents/{self.collection_name}"
        try:
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=4) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                documents = []
                if "documents" in res_data:
                    for doc in res_data["documents"]:
                        fields = doc.get("fields", {})
                        data_nettoyee = {}
                        for key, val in fields.items():
                            if "stringValue" in val:
                                data_nettoyee[key] = val["stringValue"]
                            elif "integerValue" in val:
                                data_nettoyee[key] = int(val["integerValue"])
                            elif "booleanValue" in val:
                                data_nettoyee[key] = val["booleanValue"]
                        documents.append(DocumentSimule(data_nettoyee))
                return documents
        except Exception:
            return []

class ClientFirestoreREST:
    def __init__(self, project_id):
        self.project_id = project_id
    def collection(self, name):
        return CollectionSimulee(self.project_id, name)


@st.cache_resource
def initialiser_firebase():
    if "firebase" not in st.secrets:
        st.error("❌ Les secrets Firebase sont introuvables. Vérifiez votre secrets.toml.")
        st.stop()
    project_id = st.secrets["firebase"].get("project_id")
    return ClientFirestoreREST(project_id)


# 3. GESTION DES SESSIONS ET DE LA SÉCURITÉ
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verifier_session():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "user_pseudo" not in st.session_state:
        st.session_state["user_pseudo"] = ""
    if "verifying_email" not in st.session_state:
        st.session_state["verifying_email"] = None


# Tout en haut de modules/utils.py, assurez-vous d'avoir cet import :
import requests  # 👈 AJOUTEZ CET IMPORT TOUT EN HAUT DU FICHIER

# ... (Laissez le reste du fichier intact : variables globales et client REST Firestore) ...

# 4. 🚀 SERVICE D'ENVOI DE MESSAGES UNIVERSEL ET ILLIMITÉ VIA RESEND API
def envoyer_email_brevo(destinataire_email, sujet, message_html):
    try:
        api_key = st.secrets["resend"]["api_key"]
        url = "https://resend.com"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "from": "Amicale Boule <onboarding@resend.dev>",
            "to": [destinataire_email],
            "subject": sujet,
            "html": message_html
        }
        
        # Envoi de la requête POST via la bibliothèque requests
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        # ✅ CORRECTION DE LA SYNTAXE : Validation directe du statut de succès
        if response.status_code == 200 or response.status_code == 201 or response.status_code == 202:
            return True
        else:
            st.error(f"❌ Rejet de l'API Resend (Code {response.status_code}) : {response.text}")
            
    except Exception as e:
        st.error(f"Erreur technique lors de l'envoi de l'e-mail : {e}")
    return False
