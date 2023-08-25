from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .agent import Agent

app = FastAPI()

origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class Question(BaseModel):
    text: str = Field(title="Question", description="The question to ask the model", min_length=1, max_length=1000)

class Answer(BaseModel):
    text: str

@app.post("/ask", response_model=Answer)
async def ask_question(question: Question):
    agent = Agent()
    answer, _ = agent.ask(question.text)
    return Answer(text=answer)