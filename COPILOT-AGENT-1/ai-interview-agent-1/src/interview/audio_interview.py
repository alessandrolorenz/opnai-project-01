from fastapi import UploadFile, File
from src.utils import transcrever_audio, transcrever_audio_whisper, responder_chat, sintetizar_fala, sintetizar_fala_pyttsx3
from src.utils import create_technical_challenge  # Add this import
import tempfile
import os
import base64
import soundfile as sf

def ensure_wav(input_path):
    # Só aceita arquivos WAV, senão lança erro
    if input_path.lower().endswith('.wav'):
        # Testa se é realmente um WAV válido
        try:
            with sf.SoundFile(input_path) as f:
                if f.format != 'WAV':
                    raise ValueError("Arquivo não é um WAV válido")
        except Exception as e:
            raise ValueError(f"Erro ao ler WAV: {e}")
        return input_path
    else:
        raise ValueError("Somente arquivos WAV são suportados no modo gratuito.")

async def conduct_audio_interview(audio: UploadFile, title: str, description: str, session_id: str, curriculo: str, openai_apikey: str = None):
    print("🎤 Iniciando entrevista de áudio...")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio:
        tmp_audio.write(await audio.read())
        tmp_audio_path = tmp_audio.name

    if openai_apikey:
        from src.utils import transcrever_audio, responder_chat, sintetizar_fala, create_technical_challenge
        texto = transcrever_audio(tmp_audio_path, openai_apikey)
    else:
        from src.utils import transcrever_audio_vosk, responder_chat, sintetizar_fala_pyttsx3, create_technical_challenge
        wav_path = ensure_wav(tmp_audio_path)
        texto = transcrever_audio_vosk(wav_path)

    prompt = (
        f"Currículo: {curriculo}\nResposta do candidato: {texto}"
    )
    resposta = responder_chat(prompt, session_id, title, description, openai_apikey)
    desafio = None
    if "<<END_OF_QUESTIONS>>" in resposta:
        print("🎤 Entrevista finalizada. Criando desafio técnico...")
        desafio = create_technical_challenge(description, openai_apikey)

    if openai_apikey:
        resposta_audio_path = sintetizar_fala(resposta, openai_apikey)
    else:
        resposta_audio_path = sintetizar_fala_pyttsx3(resposta)

    with open(resposta_audio_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
        audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
        audio_base64 = f"data:audio/mp3;base64,{audio_base64}"  

    result = {
        "texto": texto,
        "resposta": resposta,
        "audio_base64": audio_base64
    }
    if desafio:
        result["desafio"] = desafio
    return result

