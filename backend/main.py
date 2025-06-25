from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel
from utils import transcrever_audio, responder_chat, sintetizar_fala
import tempfile
import os
from fastapi.middleware.cors import CORSMiddleware
import base64

app = FastAPI()

# Permitir que o frontend (Next.js) faça requisições ao backend
origins = [
    "http://localhost:3000",  # Localhost para o frontend Next.js
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint para processar o áudio recebido
@app.post("/processar-audio")
async def processar_audio(audio: UploadFile = File(...)):
    # Salvar o arquivo de áudio temporariamente
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio:
        tmp_audio.write(await audio.read())
        tmp_audio_path = tmp_audio.name

    # Transcrever áudio para texto
    texto = transcrever_audio(tmp_audio_path)

    # Gerar a resposta usando GPT-3.5
    resposta = responder_chat(texto)

    # Gerar áudio com a resposta
    resposta_audio_path = sintetizar_fala(resposta)

    with open(resposta_audio_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
        audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")

    return {
        "texto": texto,
        "resposta": resposta,
        "audio_base64": audio_base64
    }

class TextRequest(BaseModel):
    texto: str

@app.post("/processar-texto")
async def processar_texto(request: TextRequest):
    texto = request.texto
    print("Texto recebido:", texto)
    resposta = responder_chat(texto)

    return {
        "resposta": resposta,
    }