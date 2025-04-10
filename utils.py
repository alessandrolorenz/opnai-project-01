from openai import OpenAI
import sounddevice as sd
import soundfile as sf
import os
import tempfile
from dotenv import load_dotenv
import keyboard

client = OpenAI()

load_dotenv()

def gravar_audio(samplerate=16100):
    import threading

    print("🕹️ Pressione BARRA DE ESPAÇO para começar a gravar, ESC para sair.")

    # Espera SPACE ou ESC
    while True:
        if keyboard.is_pressed("space"):
            break
        elif keyboard.is_pressed("esc"):
            print("🚪 Saindo...")
            exit()

    print("🎙️ Gravando... (pressione ENTER para parar)")
    gravando = True
    audio_gravado = []

    def capturar_audio():
        audio = sd.rec(int(60 * samplerate), samplerate=samplerate, channels=1)
        audio_gravado.append(audio)
        sd.wait()

    thread = threading.Thread(target=capturar_audio)
    thread.start()

    while True:
        if keyboard.is_pressed("enter"):
            print("⏸️ Parando gravação...")
            sd.stop()
            break
        elif keyboard.is_pressed("esc"):
            print("🚪 Saindo...")
            sd.stop()
            exit()

    sd.stop()
    thread.join()

    wav_path = tempfile.mktemp(suffix=".wav")
    sf.write(wav_path, audio_gravado[0], samplerate)
    print("✅ Gravação finalizada.")
    return wav_path

def transcrever_audio(caminho_arquivo):
    print("🧠 Transcrevendo áudio...")
    with open(caminho_arquivo, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return transcript.text

historico = []

def responder_chat(prompt):
    print("🤖 Gerando resposta...")

    # Adiciona a pergunta do usuário
    historico.append({"role": "user", "content": prompt})

    # Garante que o histórico tem no máximo 20 mensagens (10 interações)
    if len(historico) > 20:
        historico[:] = historico[-20:]

    # Envia o histórico para o modelo
    resposta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=historico
    )

    mensagem = resposta.choices[0].message.content

    # Adiciona a resposta da IA
    historico.append({"role": "assistant", "content": mensagem})

    # Garante o mesmo corte após a resposta
    if len(historico) > 20:
        historico[:] = historico[-20:]

    return mensagem

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

def tocar_audio(caminho_arquivo):
    print("🎧 Tocando resposta...")
    import platform
    import subprocess

    if platform.system() == "Windows":
        os.startfile(caminho_arquivo)
    elif platform.system() == "Darwin":
        subprocess.run(["open", caminho_arquivo])
    else:
        subprocess.run(["xdg-open", caminho_arquivo])
