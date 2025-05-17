# Projet 3 : Système de Transcription Audio Automatisée avec Whisper et Streamlit

## 📝 Projet réalisé par : (Binôme_12)
- ELGHIOUAN Ansam
- MAGHNOUJ Ayoub

## 📝 Encadré par :
Pr. MAHMOUDI Abdelhak

## 🔹 Description du projet
Ce projet est une application web de démonstration pour la transcription automatique de fichiers audio en texte. Elle utilise le puissant modèle **OpenAI Whisper** pour la reconnaissance vocale et une interface utilisateur interactive construite avec **Streamlit**. Ce document détaille son fonctionnement, son installation et son utilisation.

Ce projet est une application web de démonstration pour la transcription automatique de fichiers audio en texte. Elle utilise le puissant modèle **OpenAI Whisper** pour la reconnaissance vocale et une interface utilisateur interactive construite avec **Streamlit**. Ce document détaille son fonctionnement, son installation et son utilisation.

## 🌟 Fonctionnalités Principales

-   **Upload Facile de Fichiers :** Permet aux utilisateurs de téléverser des fichiers audio dans des formats courants (MP3, WAV, M4A, OGG, FLAC).
-   **Transcription Automatique :** Utilise le modèle "base" d'OpenAI Whisper pour convertir la parole contenue dans l'audio en texte.
-   **Détection Automatique de la Langue :** Identifie la langue parlée dans le fichier audio et l'affiche.
-   **Interface Utilisateur Intuitive :** Interface simple et conviviale grâce à Streamlit, guidant l'utilisateur à travers le processus.
-   **Feedback en Temps Réel :** Affiche une barre de progression pendant la transcription.
-   **Affichage Clair des Résultats :** Présente la transcription dans une zone de texte facile à lire et à copier.
-   **(Optionnel) Détails des Segments :** Possibilité d'afficher les segments de transcription avec leurs timestamps (via un expander).

## 🛠️ Technologies Utilisées

-   **Langage de Programmation :** Python 3.9+
-   **Modèle de Deep Learning :** OpenAI Whisper (modèle "base")
-   **Framework d'Interface Web :** Streamlit
-   **Gestion de l'Audio (implicite via Whisper) :** FFmpeg
-   **Gestion des Dépendances :** pip, `requirements.txt`
-   **Contrôle de Version :** Git, GitHub

## 🚀 Prérequis et Installation

Avant de commencer, assurez-vous d'avoir les éléments suivants installés sur votre système :

1.  **Python :** Version 3.9 ou ultérieure. Vous pouvez le télécharger depuis [python.org](https://www.python.org/).
2.  **pip :** Généralement inclus avec Python. Vérifiez avec `pip --version`.
3.  **Git :** Pour cloner le dépôt. Téléchargez depuis [git-scm.com](https://git-scm.com/).
4.  **FFmpeg :** **Crucial** pour le traitement audio par Whisper.
    -   **Linux (Debian/Ubuntu) :**
        ```bash
        sudo apt update && sudo apt install ffmpeg
        ```
    -   **macOS (avec Homebrew) :**
        ```bash
        brew install ffmpeg
        ```
    -   **Windows :**
        1.  Téléchargez les binaires "release essentials" depuis [ffmpeg.org/download.html](https://ffmpeg.org/download.html) (cherchez les builds de gyan.dev ou BtbN).
        2.  Décompressez l'archive (par exemple, dans `C:\ffmpeg`).
        3.  Ajoutez le dossier `bin` de FFmpeg (ex: `C:\ffmpeg\bin`) à la variable d'environnement `PATH` de votre système.

### Étapes d'Installation du Projet

1.  **Clonez ce dépôt GitHub :**
    ```bash
    git clone <URL_DE_VOTRE_DEPOT_GITHUB_ICI>
    cd projet_transcription_audio
    ```

2.  **Créez et activez un environnement virtuel Python (fortement recommandé) :**
    ```bash
    python -m venv .venv
    ```
    -   Sur Linux/macOS :
        ```bash
        source .venv/bin/activate
        ```
    -   Sur Windows (Command Prompt) :
        ```bash
        .venv\Scripts\activate.bat
        ```
    -   Sur Windows (PowerShell) :
        ```bash
        .venv\Scripts\Activate.ps1
        ```
    Vous devriez voir `(.venv)` au début de votre invite de commande.

3.  **Installez les dépendances Python :**
    ```bash
    pip install -r requirements.txt
    ```
    *Note : La première fois, cela peut prendre un certain temps pour télécharger les bibliothèques, y compris Whisper.*

## 🏃 Utilisation de l'Application

1.  Assurez-vous que votre environnement virtuel est activé et que FFmpeg est correctement installé et accessible.
2.  Depuis le répertoire racine du projet (`projet_transcription_audio`), lancez l'application Streamlit :
    ```bash
    streamlit run app.py
    ```
3.  Ouvrez votre navigateur web et accédez à l'URL affichée dans le terminal (généralement `http://localhost:8501`).
4.  L'interface de l'application s'affiche :
    *   Utilisez le widget "Choisissez un fichier audio" dans la barre latérale pour uploader un fichier audio (ex: depuis le dossier `sample_audio/`).
    *   Une fois le fichier sélectionné, vous pouvez l'écouter via le lecteur audio intégré dans la sidebar.
    *   Cliquez sur le bouton "Transcrire l'audio".
5.  Patientez pendant que la transcription est en cours (une barre de progression s'affichera).
6.  La transcription textuelle et la langue détectée apparaîtront dans la zone principale de l'application.

## 📂 Structure du Projet
projet_transcription_audio/
├── .venv/ # Environnement virtuel Python (ignoré par Git)
├── app.py # Script principal de l'application Streamlit
├── requirements.txt # Fichier listant les dépendances Python
├── sample_audio/ # Dossier pour les fichiers audio d'exemple
│ ├── exemple_francais_clair.mp3
│ └── exemple_anglais_rapide.wav
├── .gitignore # Fichier spécifiant les fichiers à ignorer par Git
└── README.md # Ce fichier de documentation

-   `app.py`: Contient tout le code de l'application Streamlit, y compris le chargement du modèle, l'interface utilisateur et la logique de transcription.
-   `requirements.txt`: Définit les bibliothèques Python nécessaires au projet.
-   `sample_audio/`: Comprend quelques fichiers audio pour tester rapidement l'application.
-   `.gitignore`: Indique à Git quels fichiers ou dossiers ignorer.
-   `README.md`: Fournit une vue d'ensemble complète du projet.

## 🖼️ Captures d'Écran de la Démo

*(Insérer ici 2-3 captures d'écran claires de l'application en fonctionnement)*

**Figure 1 : Interface principale après le lancement.**
![Interface Principale](URL_OU_CHEMIN_VERS_CAPTURE_ECRAN_1.png)

**Figure 2 : Fichier audio uploadé et prêt pour la transcription.**
![Fichier Uploadé](URL_OU_CHEMIN_VERS_CAPTURE_ECRAN_2.png)

**Figure 3 : Résultat de la transcription affiché.**
![Résultat Transcription](URL_OU_CHEMIN_VERS_CAPTURE_ECRAN_3.png)

## 📹 Vidéo de Présentation

Une vidéo de présentation détaillée (max 7 minutes) expliquant l'environnement, le code et la démo de l'application est disponible ici :
[Lien vers la vidéo de présentation (YouTube, Vimeo, ou fichier dans Google Drive)](LIEN_VERS_LA_VIDEO_ICI)

*(Si la vidéo est embarquée dans le Google Drive, le lien du Google Drive principal suffit)*

## ⚠️ Problèmes Connus et Limitations

-   La transcription de fichiers audio très longs ou de très grande taille peut être lente et consommer beaucoup de mémoire, surtout avec le modèle "base" sur CPU.
-   La précision peut diminuer en présence de bruits de fond importants, de multiples locuteurs parlant simultanément, ou d'un jargon très spécifique non présent dans les données d'entraînement de Whisper.
-   Le premier lancement de l'application peut être plus long car le modèle Whisper doit être téléchargé.
-   L'application est actuellement limitée par les capacités de la machine sur laquelle elle tourne (CPU/GPU, RAM).

## 💡 Pistes d'Amélioration Futures

-   Permettre à l'utilisateur de choisir la taille du modèle Whisper (tiny, base, small, etc.) pour un compromis vitesse/précision.
-   Intégrer la possibilité d'enregistrer l'audio directement depuis le navigateur.
-   Ajouter des options de post-traitement du texte (ex: formatage, suppression des hésitations).
-   Déployer l'application sur une plateforme plus robuste pour une utilisation à plus grande échelle (ex: Docker sur un VPS, services cloud).
-   Afficher des métriques plus détaillées sur la transcription (ex: score de confiance par segment).

---
*Ce projet a été réalisé dans le cadre du "Projet 3 - End-to-End Deep Learning".*