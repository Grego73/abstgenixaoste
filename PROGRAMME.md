# 🏆 Amicale Boule Saint-Genix Aoste - Programme de l'Application

Ce fichier sert de guide et de rappel pour l'architecture et le développement de l'application Streamlit du club.

---

## 📁 1. Architecture Finale du Projet

Le projet a été restructuré de manière modulaire pour séparer la logique technique de l'affichage des pages :

```text
📁 abstgenixaoste (Racine)
├── 📄 app.py               # Fichier principal (Routage, Navigation et Verrou global)
├── 📄 requirements.txt     # Dépendances du projet (Streamlit, Firebase-admin)
├── 📄 PROGRAMME.md         # Ce fichier (Rappel et suivi du programme)
├── 📁 modules              # LOGIQUE TECHNIQUE & SÉCURITÉ
│   ├── 📄 __init__.py      # Fichier vide pour initialiser le package
│   ├── 📄 utils.py         # Configuration Firebase et variables globales du club
│   └── 📄 auth.py          # Gestion complète (Connexion, Inscription, Récupération)
└── 📁 vues                 # INTERFACES & PAGES D'AFFICHAGE
    ├── 📄 __init__.py      # Fichier vide (Indispensable pour éviter les SyntaxError)
    ├── 📄 accueil.py       # Infos club, carte interactive et boutons GPS
    ├── 📄 actualites.py    # Résultats et lecture dynamique des concours (Firestore)
    ├── 📄 contact.py       # Formulaire de contact pour envoyer des messages (Firestore)
    └── 📄 admin.py         # Panneau de gestion sécurisé (Concours, Licences, Messages)
```

---

## 🛠️ 2. Fonctionnalités Développées & Validées

### 🔐 Sécurité & Authentification (`modules/auth.py`)
- **Hachage des mots de passe** : Sécurisation via SHA-256 avant enregistrement dans Firebase.
- **Récupération de mot de passe sécurisée** : Flux en 2 étapes avec génération d'un code temporaire à 6 chiffres (simulation e-mail).
- **Rattachement Club/Société facultatif** : Liste déroulante dynamique alimentée en temps réel par les clubs saisis par les autres membres, avec option "Autre".

### ⚙️ Gestion du Profil & Verrou Global (`app.py` & `modules/auth.py`)
- **Détecteur de première connexion** : Si un membre se connecte pour la première fois avec des champs facultatifs vides, le site se verrouille temporairement.
- **Formulaire de mise à jour forcé** : L'utilisateur doit valider ses infos ou cliquer sur *"Continuer sans rien ajouter"* pour débloquer le site.
- **Sauvegarde en Session State** : Les données du profil sont chargées une seule fois à la connexion pour **éliminer le bug de chargement infini** provoquée par les requêtes répétitives vers Firebase.

### 🛡️ Espace Gestionnaires (`vues/admin.py`)
- **Visibilité restreinte** : L'onglet apparaît dans le menu de gauche uniquement si l'utilisateur connecté possède le rôle `admin` dans Firestore.
- **Gestion des Licences** : Tableau de bord affichant les membres avec la colonne "Club" placée idéalement entre le numéro de licence et le téléphone.
- **Création de Concours** : Formulaire pour publier des événements directement dans Firestore.
- **Secrétariat** : Lecture et archivage des messages reçus via le formulaire de contact.

---

## 🚀 3. Prochaines Étapes à Prévoir (À garder en mémoire)

Voici les pistes d'améliorations que nous pourrons explorer dès que tu le souhaiteras :
1. **📧 Vrai service d'E-mails** : Remplacer l'affichage des codes de validation/récupération à l'écran par un véritable envoi d'e-mail automatique (via une API gratuite comme Brevo ou SendGrid).
2. **📂 Export de données** : Ajouter un bouton dans l'Espace Admin pour télécharger la liste des licenciés au format Excel ou CSV.
3. **💬 Système de Notification** : Alerter les administrateurs par e-mail ou notification dès qu'un nouveau message est reçu sur la page Contact.
4. **🎨 Design & Assets** : Centraliser les logos et éléments graphiques du club dans un sous-dossier dédié (ex: `assets/`).
