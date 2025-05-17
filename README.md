# Projet 3 : Système de Transcription Audio Automatisée

Ce projet est une application web de démonstration pour la transcription automatique de fichiers audio en texte. Elle utilise le puissant modèle **OpenAI Whisper** pour la reconnaissance vocale et une interface utilisateur interactive construite avec **Streamlit**.

## 📝 Projet réalisé par : (Binôme_12)
- ELGHIOUAN Ansam
- MAGHNOUJ Ayoub

## 📝 Encadré par :
- Pr. MAHMOUDI Abdelha

## 🔗 Lien de la demo sur Streamlit
- https://gr12-projet3-transcription-audio.streamlit.app/

## 📖 Définitions Clés

*   **Transcription Audio (Speech-to-Text) :** Processus de conversion de la parole contenue dans un signal audio en une séquence de mots écrits.
*   **OpenAI Whisper :** Un modèle de reconnaissance automatique de la parole (ASR) de pointe, pré-entraîné par OpenAI. Il est capable de transcrire l'audio dans de multiples langues avec une grande robustesse.
*   **Streamlit :** Un framework Python open-source qui permet de créer et de partager rapidement des applications web pour des projets de data science et de machine learning avec un minimum de code.
*   **FFmpeg :** Un projet logiciel libre de manipulation de flux audio et vidéo. Whisper l'utilise en arrière-plan pour lire et traiter une grande variété de formats audio. C'est une dépendance cruciale.
*   **Environnement Virtuel Python :** Un environnement isolé qui permet de gérer les dépendances d'un projet Python spécifique sans affecter les autres projets ou l'installation globale de Python sur le système.

## 🌟 Fonctionnalités Principales

-   **Téléversement Facile de Fichiers :** Permet aux utilisateurs de soumettre des fichiers audio dans des formats courants (MP3, WAV, M4A, OGG, FLAC).
-   **Transcription Automatique :** Utilise le modèle "base" d'OpenAI Whisper pour convertir la parole en texte.
-   **Détection Automatique de la Langue :** Identifie la langue parlée dans le fichier audio et l'affiche.
-   **Interface Utilisateur Intuitive :** Interface simple et conviviale grâce à Streamlit.
-   **Feedback en Temps Réel :** Affiche une barre de progression pendant la transcription.
-   **Affichage Clair des Résultats :** Présente la transcription dans une zone de texte facile à lire et à copier.

## 🛠️ Technologies Utilisées

-   **Langage de Programmation :** Python (version 3.8 ou ultérieure recommandée)
-   **Modèle de Deep Learning :** OpenAI Whisper (modèle "base")
-   **Framework d'Interface Web :** Streamlit
-   **Gestion de l'Audio (implicite via Whisper) :** FFmpeg
-   **Gestion des Dépendances Python :** pip (via le fichier `requirements.txt`)

## 🚀 Prérequis et Installation

Avant de commencer, assurez-vous d'avoir les éléments suivants installés sur votre système :

1.  **Python :** Version 3.8 ou ultérieure. Vous pouvez le télécharger depuis [python.org](https://www.python.org/). Assurez-vous que Python et pip sont ajoutés à votre PATH système lors de l'installation.
2.  **FFmpeg :** **Indispensable** pour le traitement audio par Whisper.
    *   **Instructions d'installation de FFmpeg :**
        *   **Windows :**
            1.  Téléchargez les binaires depuis [ffmpeg.org/download.html](https://ffmpeg.org/download.html).
            2.  Décompressez l'archive dans un dossier simple (ex: `C:\ffmpeg`).
            3.  Ajoutez le dossier `bin` de FFmpeg (ex: `C:\ffmpeg\bin`) à la variable d'environnement `PATH` de votre système.
            4.  **Important :** Après avoir modifié le PATH, redémarrez tout terminal ou invite de commande que vous utiliserez.
        *   
    *   Pour vérifier si FFmpeg est correctement installé et accessible, ouvrez un nouveau terminal et tapez `ffmpeg -version`. Vous devriez voir des informations sur la version s'afficher.

### Étapes d'Installation du Projet

1.  **Obtenez les fichiers du projet :**
    *   Téléchargez ou clonez ce projet sur votre machine locale.

2.  **Naviguez vers le dossier du projet :**
    *   Ouvrez un terminal ou une invite de commande et déplacez-vous dans le répertoire où vous avez placé les fichiers du projet (le dossier qui contient `app.py` et `requirements.txt`).

3.  **Créez et activez un environnement virtuel Python (fortement recommandé) :**
    *   Dans votre terminal, exécutez :
        ```bash
        python -m venv .venv
        ```
    *   Activez l'environnement :
        *   Sur Windows (Invite de commandes) :
            ```cmd
            .venv\Scripts\activate.bat
            ```
        *   Sur Windows (PowerShell) :
            ```powershell
            .venv\Scripts\Activate.ps1
            ```
            *(Si vous rencontrez une erreur de politique d'exécution sur PowerShell, essayez d'exécuter `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process` puis réessayez d'activer.)*
        *   Sur macOS/Linux :
            ```bash
            source .venv/bin/activate
            ```
    *   Une fois activé, votre invite de commande devrait être préfixée par `(.venv)`.

4.  **Installez les dépendances Python :**
    *   Assurez-vous que votre environnement virtuel est activé. Ensuite, exécutez :
        ```bash
        pip install -r requirements.txt
        ```
    *   *Note : La première fois, cela peut prendre un certain temps pour télécharger les bibliothèques, y compris le modèle Whisper si ce n'est pas déjà en cache.*

## 🏃 Utilisation de l'Application

1.  Assurez-vous que votre environnement virtuel est activé et que FFmpeg est correctement installé et accessible (vérifiez avec `ffmpeg -version` dans un nouveau terminal).
2.  Depuis le répertoire racine du projet (où se trouve `app.py`), lancez l'application Streamlit :
    ```bash
    streamlit run app.py
    ```
3.  Ouvrez votre navigateur web et accédez à l'URL affichée dans le terminal (généralement `http://localhost:8501`).
4.  L'interface de l'application s'affiche :
    *   Utilisez le widget "Choisissez un fichier audio" dans la barre latérale pour téléverser un fichier audio.
    *   Cliquez sur le bouton "Transcrire l'audio".
5.  Patientez pendant que la transcription est en cours.
6.  La transcription textuelle et la langue détectée apparaîtront dans la zone principale de l'application.

## 📂 Structure du Projet (Principaux Fichiers)

-   `app.py`: Script principal contenant le code de l'application Streamlit et la logique de transcription.
-   `requirements.txt`: Liste les bibliothèques Python nécessaires au fonctionnement du projet.
-   `packages.txt`: ffmpeg.
-   `screenshots/`: Capture d'écran du projet.
-   `README.md`: Ce fichier de documentation.

## 🖼️ Captures d'Écran de la Démo (Exemples)

**Figure 1 : Interface principale après le lancement.**
![aInterface Principale](/screenshots/capture1.png)

**Figure 2 : Résultat de la transcription affiché.**
![ésultat Transcription](/screenshots/capture2.png)

## 📹 Vidéo de Présentation

La vidéo de présentation expliquant l'environnement, le code et la démo de l'application est disponible ici :
[Lien vers la vidéo de présentation sur Google Drive](drive.google.com/video)

---
*Ce projet a été réalisé dans le cadre du "Projet 3 - End-to-End Deep Learning" par Mme Ansam EL GHIOUAN et Mr Ayoub MAGHNOUJ.*