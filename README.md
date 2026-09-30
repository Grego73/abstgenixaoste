# 🏆 Application de l'Amicale Boule Saint-Genix Aoste

Bienvenue sur l'application officielle de l'**Amicale Boule Saint-Genix Aoste** (Association de Sport-Boules / Boule Lyonnaise fondée en 2004). Cette plateforme permet aux membres de suivre l'actualité du club, de contacter le secrétariat et d'accéder à un espace membre sécurisé lié à une base de données Firebase Firestore.

---

## 🚀 Démarrage Rapide

Cette application est configurée pour fonctionner instantanément dans un environnement de développement conteneurisé (DevContainer).

### Option 1 : Via GitHub Codespaces (Recommandé & Ultra Simple)
1. Ouvrez ce dépôt sur votre compte GitHub.
2. Cliquez sur le bouton vert **Code**, puis allez sur l'onglet **Codespaces**.
3. Cliquez sur **Create codespace on main**.
4. Attendez que l'environnement s'initialise. L'application Streamlit se lancera **automatiquement** dans un onglet de votre navigateur.

### Option 2 : En local avec VS Code & Docker
1. Clonez ce dépôt sur votre machine.
2. Ouvrez le dossier avec **VS Code**.
3. Assurez-vous d'avoir installé l'extension **Dev Containers** de Microsoft et d'avoir **Docker** démarré.
4. Cliquez sur la notification en bas à droite *"Reopen in Container"*.
5. Une fois le conteneur prêt, l'application démarre toute seule sur le port `8501`.

### Option 3 : En local sans Docker (Manuel)
Si vous préférez la lancer manuellement sur votre machine :
```bash
# 1. Installez les dépendances
pip install -r requirements.txt

# 2. Lancez l'application
streamlit run app.py
```

---

## 🔑 Configuration des Secrets (Firebase)

Pour que l'application puisse communiquer avec la base de données Firestore, vous devez ajouter vos identifiants Firebase dans les secrets Streamlit.

Créez un fichier `.streamlit/secrets.toml` (si vous travaillez en local sans Docker) ou configurez-le dans vos variables d'environnement sous cette forme :

```toml
[firebase]
type = "service_account"
project_id = "VOTRE_PROJECT_ID"
private_key_id = "VOTRE_PRIVATE_KEY_ID"
private_key = "-----BEGIN PRIVATE KEY-----\nVOTRE_CLE_PRIVEE\n-----END PRIVATE KEY-----\n"
client_email = "VOTRE_CLIENT_EMAIL"
```

---

## 📁 Structure Globale du Projet

Le code respecte une architecture modulaire stricte :
* `app.py` : Point d'entrée de l'application, gère la navigation et le verrou global de sécurité.
* `modules/` : Contient la logique technique (initialisation Firebase dans `utils.py`, formulaires de sécurité dans `auth.py`).
* `vues/` : Regroupe les différentes pages d'affichage (`accueil.py`, `actualites.py`, `contact.py`, `admin.py`).

---

## 🛡️ Attribution des Droits Administrateur

Par défaut, tout nouvel inscrit possède le rôle `membre`. Pour accéder au **Panneau Administration** :
1. Rendez-vous sur votre console **Firebase Firestore**.
2. Allez dans la collection `users` et sélectionnez le document portant le **Pseudo** du compte à modifier.
3. Ajoutez un champ (Add Field) :
   * Nom du champ : `role`
   * Type : `string`
   * Valeur : `admin`
4. Reconnectez-vous sur l'application pour voir apparaître l'onglet sécurisé.
