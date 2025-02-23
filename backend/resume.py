from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai
import os
from dotenv import load_dotenv

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ratemyresu.me","http://localhost:3000"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Gemini configuration
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash')


# Tailor Resume
class TailorRequest(BaseModel):
    job_description: str
    resume_bullet: str

@app.post("/tailor-resume")
def tailor_resume(request: TailorRequest):
    prompt = f"""Be concise and do not include unnecessary text or formatting or bullets. Concisely provide a single tailored resume bullet point based on the provided original bullet to be more relevant to the job requirements provided. 

    Job Requirements: {request.job_description}
    Original Bullet: {request.resume_bullet}"""
    
    response = model.generate_content(prompt)
    
    return {"tailored_bullet": response.text}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)