import streamlit as st
import whisper
import os
import tempfile # Pour gérer les fichiers temporaires de manière sécurisée

# --- Configuration de la Page Streamlit ---
st.set_page_config(
    page_title="Transcription Audio Pro",
    page_icon="🎙️",
    layout="wide", # "centered" ou "wide"
    initial_sidebar_state="expanded", # "auto", "expanded", "collapsed"
    menu_items={
        'Get Help': 'https://github.com/openai/whisper/discussions', # Lien d'aide
        'Report a bug': "mailto:votre.email@example.com", # Pour rapporter un bug
        'About': """
        ## Application de Transcription Audio Automatique (Projet 3)
        Cette application utilise le modèle **OpenAI Whisper** pour transcrire des fichiers audio.
        Développé avec Streamlit.
        """
    }
)

# --- Fonctions Utilitaires ---
@st.cache_resource # Important pour ne pas recharger le modèle à chaque interaction
def load_whisper_model():
    """Charge le modèle Whisper. 'base' est un bon compromis."""
    # Options de modèles: "tiny", "base", "small", "medium", "large"
    # "base.en" ou "small.en" pour des modèles uniquement anglais plus rapides.
    try:
        model = whisper.load_model("base")
        return model
    except Exception as e:
        st.error(f"Erreur lors du chargement du modèle Whisper : {e}")
        st.error("Assurez-vous d'avoir une connexion internet pour le premier téléchargement du modèle.")
        st.error("Vérifiez également l'espace disque disponible.")
        return None

# --- Chargement du Modèle ---
# Ce bloc est exécuté une seule fois grâce au cache_resource
with st.spinner("Chargement du modèle de transcription (cela peut prendre un moment au premier lancement)..."):
    model = load_whisper_model()

if model is None:
    st.stop() # Arrête l'exécution du script si le modèle n'a pas pu être chargé

# --- Interface Utilisateur (UI) ---
st.title("🎙️ Projet 3 : Système de Transcription Audio Automatique")
st.markdown("""
Bienvenue ! Cette application vous permet de transcrire le contenu audio de vos fichiers.
1.  **Uploadez un fichier audio** via la barre latérale. Formats supportés : MP3, WAV, M4A, OGG, FLAC.
2.  Cliquez sur le bouton **"Transcrire l'audio"**.
3.  La transcription apparaîtra ci-dessous.
""")
st.markdown("---")

# --- Barre Latérale pour les Contrôles ---
st.sidebar.header("⚙️ Contrôles")
uploaded_file = st.sidebar.file_uploader(
    "1. Choisissez un fichier audio :",
    type=["wav", "mp3", "m4a", "ogg", "flac"],
    help="Formats supportés : WAV, MP3, M4A, OGG, FLAC. Taille max : 200MB (limite Streamlit par défaut)."
)

transcribe_button_disabled = uploaded_file is None
transcribe_button = st.sidebar.button(
    "2. Transcrire l'audio",
    disabled=transcribe_button_disabled,
    type="primary", # Rend le bouton plus visible
    use_container_width=True # Fait que le bouton prend toute la largeur de la sidebar
)

if uploaded_file is not None:
    st.sidebar.subheader("Fichier audio sélectionné :")
    st.sidebar.write(f"Nom : `{uploaded_file.name}`")
    st.sidebar.write(f"Type : `{uploaded_file.type}`")
    st.sidebar.write(f"Taille : `{uploaded_file.size / (1024*1024):.2f} MB`")
    st.sidebar.audio(uploaded_file, format=uploaded_file.type)
else:
    st.sidebar.info("Veuillez d'abord uploader un fichier audio.")

st.sidebar.markdown("---")
st.sidebar.markdown("### Ressources")
st.sidebar.markdown("- [Documentation Streamlit](https://docs.streamlit.io)")
st.sidebar.markdown("- [OpenAI Whisper sur GitHub](https://github.com/openai/whisper)")
st.sidebar.markdown("---")
st.sidebar.caption("Application réalisée pour le Projet 3.")


# --- Logique de Transcription et Affichage des Résultats ---
if transcribe_button and uploaded_file is not None:
    st.subheader("🔍 Processus de Transcription")
    progress_bar = st.progress(0, text="Initialisation...")

    temp_audio_path = None # Initialiser pour le bloc finally
    try:
        # Sauvegarder temporairement le fichier uploadé car Whisper attend un chemin de fichier
        # Utiliser tempfile pour une gestion sécurisée des fichiers temporaires
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            temp_audio_path = tmp_file.name

        progress_bar.progress(25, text="Fichier audio préparé. Lancement de la transcription Whisper...")
        st.write(f"Fichier temporaire créé : `{temp_audio_path}` (sera supprimé après traitement)")

        # Transcrire l'audio
        # fp16=False est plus sûr pour la compatibilité CPU. Mettre à True si GPU disponible et compatible.
        options = whisper.DecodingOptions(fp16=False) # Peut ajouter language="fr" pour forcer une langue
        result = model.transcribe(temp_audio_path, **vars(options))

        transcription_text = result["text"]
        detected_language = result["language"]

        progress_bar.progress(75, text="Transcription terminée. Affichage des résultats...")

        st.subheader("📄 Transcription Résultante :")
        st.text_area(
            label="Texte transcrit :",
            value=transcription_text,
            height=300,
            help="Vous pouvez copier ce texte."
        )
        st.info(f"🌐 Langue détectée par le modèle : **{detected_language.upper()}**")

        # Optionnel: Afficher plus de détails du résultat de Whisper
        with st.expander("Voir les détails de la transcription (segments)"):
            st.json(result["segments"])

        progress_bar.progress(100, text="Terminé !")
        st.success("Transcription effectuée avec succès !")

    except Exception as e:
        st.error(f"❌ Une erreur est survenue durant la transcription :")
        st.exception(e) # Affiche l'erreur complète avec la trace
        if progress_bar: # Si la barre de progression existe
             progress_bar.progress(100, text="Erreur rencontrée.")
    finally:
        # Nettoyage : Supprimer le fichier temporaire après usage
        if temp_audio_path and os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
            # st.write(f"Fichier temporaire `{temp_audio_path}` supprimé.") # Pour débogage

elif transcribe_button and uploaded_file is None:
    st.warning("⚠️ Veuillez d'abord uploader un fichier audio avant de cliquer sur 'Transcrire'.")

# Message initial si aucun fichier n'est encore traité
if not transcribe_button or uploaded_file is None:
     st.info("☝️ Uploadez un fichier audio et cliquez sur 'Transcrire l'audio' pour voir les résultats ici.")