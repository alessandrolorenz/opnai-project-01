from pydantic import BaseModel
from typing import List, Optional

class JobDescription(BaseModel):
    title: str
    description: str
    technologies: List[str]

class InterviewScriptResponse(BaseModel):
    script: str

class AudioInterviewResponse(BaseModel):
    audio_url: str
    transcript: str
    answer: str
    challenge: Optional[str] = None

class TechChallengeResponse(BaseModel):
    challenge: str
    solution: Optional[str] = None

class AudioInterviewRequest(BaseModel):
    title: str
    description: str