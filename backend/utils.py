from openai import OpenAI
import os
import tempfile
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Transcrição com Whisper
def transcrever_audio(caminho_arquivo):
    print("🧠 Transcrevendo áudio...")
    with open(caminho_arquivo, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return response.text

# Histórico de conversa
historico = []

def responder_chat(prompt):
    print("🤖 Gerando resposta...")
    historico.append({"role": "user", "content": prompt})

    if len(historico) > 20:
        historico[:] = historico[-20:]

    resposta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=historico
    )

    mensagem = resposta.choices[0].message.content
    historico.append({"role": "assistant", "content": mensagem})

    if len(historico) > 20:
        historico[:] = historico[-20:]

    return mensagem

# TTS com voz da OpenAI
def sintetizar_fala(texto):
    print("🔊 Convertendo texto em fala...")
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=texto,
    )
    mp3_path = tempfile.mktemp(suffix=".mp3")
    with open(mp3_path, "wb") as f:
        f.write(response.content)
    return mp3_path
