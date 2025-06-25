from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from src.models.schemas import JobDescription, InterviewScriptResponse, AudioInterviewResponse
from src.interview.script_generator import generate_script
from src.interview.audio_interview import conduct_audio_interview
from src.interview.tech_challenge import create_tech_challenge

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.post("/generate-script", response_model=InterviewScriptResponse)
# async def generate_interview_script(job_description: JobDescription):
#     print("📝 Gerando roteiro de entrevista...")
#     script = generate_script(job_description.description)
#     return {"script": script}

@app.post("/conduct-audio-interview", response_model=AudioInterviewResponse)
async def audio_interview(
    audio: UploadFile = File(...),
    title: str = Form(...),
    description: str = Form(...),
    session_id: str = Form(...),
    curriculo: str = Form(...),
    openai_apikey: str = Form(None)
    ):
    result = await conduct_audio_interview(audio, title, description, session_id, curriculo, openai_apikey)
    return AudioInterviewResponse(
        audio_url=result["audio_base64"],
        transcript=result["texto"],
        answer=result["resposta"],
        challenge=result.get("desafio", None)
    )

@app.post("/create-tech-challenge", response_model=InterviewScriptResponse)
async def tech_challenge(job_description: JobDescription):
    challenge = create_tech_challenge(job_description.description)
    return {"challenge": challenge}