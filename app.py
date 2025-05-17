import streamlit as st
import whisper
import os
import tempfile
import numpy as np # Nécessaire pour manipuler les données audio de streamlit-webrtc
from scipy.io.wavfile import write as write_wav # Pour sauvegarder l'audio enregistré en WAV
from streamlit_webrtc import webrtc_streamer, WebRtcMode, AudioProcessorBase # Composants pour l'enregistrement

# --- Configuration de la Page Streamlit ---
st.set_page_config(
    page_title="Transcription Audio Pro",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/openai/whisper/discussions',
        'Report a bug': "mailto:votre.email@example.com",
        'About': """
        ## Application de Transcription Audio Automatique (Projet 3)
        Cette application utilise le modèle **OpenAI Whisper** pour transcrire des fichiers audio.
        Développé avec Streamlit.
        """
    }
)

# --- Fonctions Utilitaires ---
@st.cache_resource
def load_whisper_model():
    try:
        model = whisper.load_model("base")
        return model
    except Exception as e:
        st.error(f"Erreur lors du chargement du modèle Whisper : {e}")
        return None

# --- Classe pour le traitement audio de streamlit-webrtc ---
# Elle va accumuler les trames audio reçues du navigateur
class AudioRecorder(AudioProcessorBase):
    def __init__(self) -> None:
        super().__init__()
        self._frames_list = [] # Liste pour stocker les trames audio
        self.sample_rate = 16000 # Fréquence d'échantillonnage (Whisper préfère 16kHz)
                                 # Note: le navigateur peut envoyer à une autre fréquence,
                                 # une conversion pourrait être nécessaire si ce n'est pas géré par webrtc_streamer

    def recv(self, frame):
        # frame est un objet av.AudioFrame
        # On convertit les données audio en un array numpy
        # Les données sont typiquement en int16
        # frame.layout.name donne le format (ex: 'mono', 'stereo')
        # frame.sample_rate donne la fréquence d'échantillonnage
        # st.write(f"Received frame: {frame.format.name}, {frame.sample_rate}Hz, {len(frame.planes[0])} bytes")
        self.sample_rate = frame.sample_rate # Met à jour avec la vraie fréquence
        self._frames_list.append(frame.to_ndarray(format="s16", layout="flat"))
        return frame # Doit retourner la trame

    def get_recorded_data(self):
        if not self._frames_list:
            return None, None
        # Concaténer toutes les trames
        audio_data = np.concatenate(self._frames_list, axis=0)
        return audio_data, self.sample_rate

    def reset_frames(self):
        self._frames_list = []


# --- Chargement du Modèle ---
with st.spinner("Chargement du modèle de transcription..."):
    model = load_whisper_model()

if model is None:
    st.stop()

# --- Variables d'état de session pour gérer l'audio enregistré ---
if "audio_buffer" not in st.session_state:
    st.session_state.audio_buffer = None
if "sample_rate_buffer" not in st.session_state:
    st.session_state.sample_rate_buffer = None
if "transcription_output" not in st.session_state:
    st.session_state.transcription_output = ""
if "detected_language_output" not in st.session_state:
    st.session_state.detected_language_output = ""


# --- Interface Utilisateur (UI) ---
st.title("🎙️ Projet 3 : Système de Transcription Audio Automatique")
st.markdown("""
Bienvenue ! Cette application vous permet de transcrire des fichiers audio ou d'enregistrer directement depuis votre microphone.
""")
st.markdown("---")

# --- Options d'entrée : Upload ou Enregistrement ---
input_method = st.radio(
    "Choisissez votre source audio :",
    ("Téléverser un fichier", "Enregistrer depuis le microphone"),
    horizontal=True,
    key="input_method_radio"
)

# Colonnes pour une meilleure mise en page
col1, col2 = st.columns([0.6, 0.4]) # Zone de transcription plus large

with col2: # Colonne de droite pour les contrôles
    st.subheader("⚙️ Contrôles")

    if input_method == "Téléverser un fichier":
        st.markdown("#### 1. Téléverser un fichier audio")
        uploaded_file = st.file_uploader(
            "Choisissez un fichier :",
            type=["wav", "mp3", "m4a", "ogg", "flac"],
            help="Formats supportés : WAV, MP3, M4A, OGG, FLAC.",
            label_visibility="collapsed"
        )

        if uploaded_file is not None:
            st.write(f"Fichier sélectionné : `{uploaded_file.name}`")
            st.audio(uploaded_file, format=uploaded_file.type)
            audio_to_transcribe = uploaded_file
        else:
            st.info("Veuillez téléverser un fichier audio.")
            audio_to_transcribe = None

    elif input_method == "Enregistrer depuis le microphone":
        st.markdown("#### 1. Enregistrer l'audio")
        st.info("Cliquez sur 'START' pour commencer l'enregistrement. Le navigateur vous demandera l'autorisation d'utiliser le microphone.")

        # webrtc_ctx contiendra l'état du streamer, y compris l'AudioProcessor
        webrtc_ctx = webrtc_streamer(
            key="audio-recorder",
            mode=WebRtcMode.SENDONLY, # On envoie seulement l'audio du client vers le serveur
            audio_processor_factory=AudioRecorder, # Notre classe pour traiter l'audio
            media_stream_constraints={"audio": True, "video": False}, # On ne veut que l'audio
            # sendback_audio=False # Pas besoin de renvoyer l'audio au client
        )

        if webrtc_ctx.state.playing and webrtc_ctx.audio_processor:
            st.info("🔴 Enregistrement en cours... Cliquez sur 'STOP' pour arrêter.")
            # Bouton pour explicitement sauvegarder l'enregistrement (optionnel, car on peut le faire au stop)
        elif not webrtc_ctx.state.playing and webrtc_ctx.audio_processor:
            # L'enregistrement est arrêté, on récupère les données
            audio_data, sample_rate = webrtc_ctx.audio_processor.get_recorded_data()
            if audio_data is not None and sample_rate is not None:
                st.session_state.audio_buffer = audio_data
                st.session_state.sample_rate_buffer = sample_rate
                st.success("Enregistrement terminé et sauvegardé en mémoire.")
                st.audio(data=audio_data, sample_rate=sample_rate, format="audio/wav")
                # Important: réinitialiser les frames pour le prochain enregistrement
                webrtc_ctx.audio_processor.reset_frames()
            elif st.session_state.audio_buffer is not None:
                 st.info("Un enregistrement précédent est disponible. Cliquez sur 'Transcrire'.")
                 st.audio(data=st.session_state.audio_buffer, sample_rate=st.session_state.sample_rate_buffer, format="audio/wav")

        audio_to_transcribe = st.session_state.audio_buffer


    st.markdown("#### 2. Lancer la Transcription")
    transcribe_button_disabled = audio_to_transcribe is None
    if st.button(
        "Transcrire l'audio",
        disabled=transcribe_button_disabled,
        type="primary",
        use_container_width=True
    ):
        if audio_to_transcribe is not None:
            st.session_state.transcription_output = "" # Réinitialiser
            st.session_state.detected_language_output = "" # Réinitialiser
            progress_bar = st.progress(0, text="Initialisation...")
            temp_audio_path = None
            try:
                if hasattr(audio_to_transcribe, 'name'): # C'est un fichier uploadé
                    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(audio_to_transcribe.name)[1]) as tmp_file:
                        tmp_file.write(audio_to_transcribe.getvalue())
                        temp_audio_path = tmp_file.name
                elif isinstance(audio_to_transcribe, np.ndarray): # C'est un buffer numpy (audio enregistré)
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                        # Écrire le numpy array en fichier WAV temporaire
                        # Whisper attend 16kHz, s16, mono. Si ce n'est pas le cas, ffmpeg essaiera de convertir.
                        # Pour être sûr, on pourrait convertir ici, mais laissons ffmpeg/whisper tenter.
                        # Assurez-vous que les données sont bien en int16.
                        # Si elles sont en float, multipliez par 32767 et convertissez en int16.
                        # Ici, on suppose que AudioRecorder retourne déjà du s16 (int16).
                        write_wav(tmp_file.name, st.session_state.sample_rate_buffer, audio_to_transcribe.astype(np.int16))
                        temp_audio_path = tmp_file.name
                else:
                    st.error("Type de source audio non reconnu.")
                    st.stop()

                progress_bar.progress(25, text="Préparation... Lancement de la transcription Whisper...")

                options = whisper.DecodingOptions(fp16=False)
                result = model.transcribe(temp_audio_path, **vars(options))

                st.session_state.transcription_output = result["text"]
                st.session_state.detected_language_output = result["language"]

                progress_bar.progress(100, text="Terminé !")
                st.success("Transcription effectuée avec succès !")

            except Exception as e:
                st.error(f"❌ Une erreur est survenue durant la transcription :")
                st.exception(e)
                if 'progress_bar' in locals():
                     progress_bar.progress(100, text="Erreur rencontrée.")
            finally:
                if temp_audio_path and os.path.exists(temp_audio_path):
                    os.remove(temp_audio_path)
        else:
            st.warning("⚠️ Veuillez d'abord fournir un audio (uploader ou enregistrer).")


    st.sidebar.markdown("---")
    st.sidebar.markdown("### Ressources")
    st.sidebar.markdown("- [Github repo](https://github.com/Ayyyyoub/gr12-projet3-transcription-audio)")
    st.sidebar.markdown("- [Documentation Streamlit](https://docs.streamlit.io)")
    st.sidebar.markdown("- [OpenAI Whisper sur GitHub](https://github.com/openai/whisper)")
    st.sidebar.markdown("- [Streamlit-WebRTC](https://github.com/whitphx/streamlit-webrtc)")
    st.sidebar.markdown("---")
    st.sidebar.caption("Application réalisée pour le Projet 3")
    st.sidebar.caption("par Ansam EL GHIOUAN et Ayoub MAGHNOUJ.")

with col1: # Colonne de gauche pour les résultats
    st.subheader("🔍 Résultats de la Transcription")
    if st.session_state.transcription_output:
        st.text_area(
            label="Texte transcrit :",
            value=st.session_state.transcription_output,
            height=300,
            help="Vous pouvez copier ce texte."
        )
        st.info(f"🌐 Langue détectée par le modèle : **{st.session_state.detected_language_output.upper()}**")
    else:
        st.info("☝️ Les résultats de la transcription apparaîtront ici.")