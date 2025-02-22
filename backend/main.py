# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

app = FastAPI()

# Configure Ollama - connects to localhost:11434
llm = Ollama(base_url="http://localhost:11434", model="tinyllama:latest")

class TailorRequest(BaseModel):
    job_description: str
    resume_bullet: str

@app.post("/tailor-resume")
async def tailor_resume(request: TailorRequest):
    prompt = PromptTemplate.from_template("""
    <s>[INST] Revise this resume bullet point to better match the job requirements.
    Focus on aligning skills and keywords from the job description.

    Job Description: {job_desc}
    Original Bullet: {bullet}
    
    Improved Bullet: [/INST]
    """)
    
    chain = LLMChain(llm=llm, prompt=prompt)
    result = chain.invoke({
        "job_desc": request.job_description,
        "bullet": request.resume_bullet
    })
    
    return {"tailored_bullet": result["text"]}