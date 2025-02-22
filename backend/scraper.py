# services/scraper.py
import requests
from bs4 import BeautifulSoup

def scrape_indeed_jobs(query: str):
    url = f"https://ca.indeed.com/jobs?q={query.replace(' ', '+')}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    return [{
        "title": job.select_one(".jobTitle").text.strip(),
        "company": job.select_one(".companyName").text.strip(),
        "description": job.select_one(".job-snippet").text.strip()
    } for job in soup.select(".jobCard")]