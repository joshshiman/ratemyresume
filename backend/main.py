from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from supabase import create_client
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

# Initialize FastAPI app
app = FastAPI()

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ratemyresu.me", "http://localhost:3000"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Gemini configuration
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash')

# Function to scrape job details
def scrape_job_details(job_url: str):
    response = requests.get(job_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract basic information
    title = soup.find('span', {'property': 'title'}).text.strip() if soup.find('span', {'property': 'title'}) else ''
    company = soup.find('span', {'property': 'name'}).text.strip() if soup.find('span', {'property': 'name'}) else ''
    location = soup.find('span', {'property': 'addressLocality'}).text.strip() if soup.find('span', {'property': 'addressLocality'}) else ''

    # Extract and flatten salary information
    pay_element = soup.find('span', {'property': 'baseSalary'})
    pay_text = ""
    if pay_element:
        parts = []
        if pay_element.find('span', {'property': 'minValue'}):
            parts.append(f"Min: {pay_element.find('span', {'property': 'minValue'}).text.strip()}")
        if pay_element.find('span', {'property': 'maxValue'}):
            parts.append(f"Max: {pay_element.find('span', {'property': 'maxValue'}).text.strip()}")
        if pay_element.find('span', {'property': 'unitText'}):
            parts.append(f"Unit: {pay_element.find('span', {'property': 'unitText'}).text.strip()}")
        pay_text = " | ".join(parts)

    # Improved description extraction
    description_parts = []
    main_section = soup.find('div', class_='main-job-posting-detail')
    
    if main_section:
        current_section = None
        for element in main_section.find_all(['h3', 'h4', 'div', 'ul', 'p']):
            if element.name in ['h3', 'h4']:
                # Start new section
                current_section = element.text.strip()
                description_parts.append(f"\n{current_section}:")
            elif element.name == 'ul':
                # List items
                items = [li.text.strip() for li in element.find_all('li')]
                if items:
                    description_parts.append("\n- " + "\n- ".join(items))
            elif element.name == 'p':
                # Paragraph text
                text = element.text.strip()
                if text:
                    description_parts.append(f"\n{text}")
            elif element.name == 'div' and element.get('property'):
                # Special sections
                section_title = element.find_previous(['h3', 'h4'])
                if section_title:
                    section_title = section_title.text.strip()
                    items = [li.text.strip() for li in element.find_all('li')]
                    if not items:
                        items = [p.text.strip() for p in element.find_all('p')]
                    if items:
                        description_parts.append(f"\n{section_title}:\n- " + "\n- ".join(items))

    # Join all parts and clean up empty lines
    description_text = "\n".join([p.strip() for p in description_parts if p.strip()])

    return {
        'title': title,
        'company': company,
        'location': location,
        'pay': pay_text,
        'description': description_text,
        'source_url': job_url
    }

# Route to scrape and save jobs
@app.get("/scrape-jobs")
def scrape_and_save_jobs(query: str):
    base_url = "https://www.jobbank.gc.ca"
    # Ensure spaces in the query are replaced with '+' to fit URL encoding
    search_url = f"{base_url}/jobsearch/jobsearch?searchstring={query.replace(' ', '+')}"
    
    # Perform GET request to scrape job listings
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    jobs = []
    for job_link in soup.select('a.resultJobItem'):
        job_path = job_link['href']
        full_url = urljoin(base_url, job_path)
        
        try:
            job_data = scrape_job_details(full_url)
            # Insert job details directly to Supabase
            supabase.table('jobs').insert(job_data).execute()
            jobs.append(job_data)
        except Exception as e:
            print(f"Error processing {full_url}: {str(e)}")
            continue
    
    return {
        "message": f"Successfully added {len(jobs)} jobs",
        "count": len(jobs)
    }

# Route to get jobs
@app.get("/jobs")
def get_jobs(page: int = 1, limit: int = 1):
    try:
        offset = (page - 1) * limit
        response = supabase.table('jobs') \
            .select("*") \
            .range(offset, offset + limit - 1) \
            .execute()
        
        return {
            "jobs": response.data,
            "page": page,
            "limit": limit
        }
    except Exception as e:
        return {"error": str(e)}

# Tailor Resume request model
class TailorRequest(BaseModel):
    job_description: str
    resume_bullet: str

# Route to tailor resume
@app.post("/tailor-resume")
def tailor_resume(request: TailorRequest):
    prompt = f"""Be concise and do not include unnecessary text or formatting or bullets. Concisely provide a single tailored resume bullet point based on the provided original bullet to be more relevant to the job requirements provided. 

    Job Requirements: {request.job_description}
    Original Bullet: {request.resume_bullet}"""
    
    response = model.generate_content(prompt)
    
    return {"tailored_bullet": response.text}

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)