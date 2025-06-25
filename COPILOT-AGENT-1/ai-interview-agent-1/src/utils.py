from openai import OpenAI
import os
import tempfile
from dotenv import load_dotenv
import pyttsx3
# import whisper
from vosk import Model, KaldiRecognizer
import wave
import json

load_dotenv()
def get_openai_client(api_key=None):
    if api_key:
        return OpenAI(api_key=api_key)
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_interview_script(job_description, api_key=None):
    client = get_openai_client(api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"Generate an interview script based on the following job description: {job_description}"}
        ]
    )
    return response.choices[0].message.content

def conduct_audio_interview(audio_file_path, api_key=None):
    client = get_openai_client(api_key)
    with open(audio_file_path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return response.text

def create_technical_challenge(job_description, api_key=None):
    client = get_openai_client(api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"Create a technical challenge based on the following job description: {job_description}"}
        ]
    )
    return response.choices[0].message.content

# Transcrição com Whisper
def transcrever_audio(caminho_arquivo, api_key=None):
    print("🧠 Transcrevendo áudio...")
    client = get_openai_client(api_key)
    with open(caminho_arquivo, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return response.text

def transcrever_audio_whisper(caminho_arquivo):
    print("🧠 Transcrevendo áudio localmente...")
    model = whisper.load_model("base")  # ou "small", "medium", "large"
    result = model.transcribe(caminho_arquivo, language="pt")
    return result["text"]

model = Model("vosk-model-small-pt-0.3")  # Carregue o modelo uma vez
modelEn = Model("vosk-model-small-en-us-0.15")  # Carregue o modelo em inglês se necessário
def transcrever_audio_vosk(caminho_arquivo):
    wf = wave.open(caminho_arquivo, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())
    texto = ""
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())
            texto += res.get("text", "") + " "
    res = json.loads(rec.FinalResult())
    texto += res.get("text", "")
    return texto.strip()

# Histórico de conversa por sessão
historicos = {}

def responder_chat(prompt, session_id, vaga, descricao, api_key=None):
    print("🤖 Gerando resposta...")
    if session_id not in historicos:
        historicos[session_id] = [{
            "role": "system",
            "content": (
                "Você é um recrutador de RH. Sua tarefa é conduzir uma entrevista de emprego com um candidato. "
                "Você deve fazer perguntas relevantes baseadas na vaga e descrição fornecidas."
                f"A vaga é: {vaga} e a descrição é: {descricao}."
                "A vaga e a descrição serão fornecidas. Faça perguntas relevantes, seja cordial e mantenha o foco na avaliação do candidato para a vaga."
                "Você ira seguir um roteiro de entrevista com perguntas específicas."
                "Deverá fazer sómente uma pergunta e esperar a resposta do candidato antes de fazer a próxima pergunta."
                "Não repita perguntas"
                "Não valide as respostas apenas siga o fluxo até o fim da entrevista."
                "Para ser breve, sempre ao fim de tres perguntas finalize a entrevista."
                "Ao final, informe que finalizou as perguntas e forneça um desafio técnico relacionado à vaga."
                "Quando você finalizar as perguntas da entrevista, responda exatamente com a frase <<END_OF_QUESTIONS>> antes de qualquer comentário final."
                "Avalie a resposta do desafio e depois reinicie a entrevista novamente se o candidato quiser continuar."
            )
        }, {"role": "user", "content": prompt}]
    else:
        historicos[session_id].append({"role": "user", "content": prompt})

    if len(historicos[session_id]) > 20:
        historicos[session_id] = historicos[session_id][-20:]

    client = get_openai_client(api_key)
    resposta = client.chat.completions.create(
        model="gpt-4o",
        messages=historicos[session_id]
    )
    mensagem = resposta.choices[0].message.content
    historicos[session_id].append({"role": "assistant", "content": mensagem})

    if len(historicos[session_id]) > 20:
        historicos[session_id] = historicos[session_id][-20:]

    return mensagem

# TTS com voz da OpenAI
def sintetizar_fala(texto, api_key=None):
    print("🔊 Convertendo texto em fala...")
    client = get_openai_client(api_key)
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=texto,
    )
    mp3_path = tempfile.mktemp(suffix=".mp3")
    with open(mp3_path, "wb") as f:
        f.write(response.content)
    return mp3_path

def sintetizar_fala_pyttsx3(texto):
    print("🔊 Convertendo texto em fala localmente (pyttsx3)...")
    engine = pyttsx3.init()
    mp3_path = tempfile.mktemp(suffix=".mp3")
    engine.save_to_file(texto, mp3_path)
    engine.runAndWait()
    return mp3_path
