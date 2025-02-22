from fastapi import FastAPI
from pydantic import BaseModel
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

app = FastAPI()

# Configuration
LLM = Ollama(base_url="http://localhost:11434", model="tinyllama")

class TailorRequest(BaseModel):
    job_description: str
    resume_bullet: str

@app.post("/tailor-resume")
def tailor_resume(request: TailorRequest):
    prompt = PromptTemplate.from_template("""
    [INST] Improve this resume bullet for job requirements:
    {job_desc}
    
    Original: {bullet}
    Revised: [/INST]
    """)
    
    return {"tailored_bullet": LLMChain(
        llm=LLM,
        prompt=prompt
    ).invoke({
        "job_desc": request.job_description,
        "bullet": request.resume_bullet
    })["text"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)