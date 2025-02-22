from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

app = FastAPI()

def scrape_job_details(job_url: str):
    response = requests.get(job_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract basic information
    title = soup.find('span', {'property': 'title'}).text.strip() if soup.find('span', {'property': 'title'}) else ''
    company = soup.find('span', {'property': 'name'}).text.strip() if soup.find('span', {'property': 'name'}) else ''
    location = soup.find('span', {'property': 'addressLocality'}).text.strip() if soup.find('span', {'property': 'addressLocality'}) else ''
    
    # Extract salary information
    pay_element = soup.find('span', {'property': 'baseSalary'})
    pay = {
        'currency': 'CAD',
        'min': pay_element.find('span', {'property': 'minValue'}).text.strip() if pay_element else None,
        'max': pay_element.find('span', {'property': 'maxValue'}).text.strip() if pay_element else None,
        'unit': pay_element.find('span', {'property': 'unitText'}).text.strip() if pay_element else None
    } if pay_element else None

    # Extract detailed job description components
    description_sections = {}
    for section in soup.find_all('div', {'property': True}):
        prop = section['property']
        if prop in ['responsibilities', 'skills', 'experienceRequirements', 'jobBenefits']:
            section_title = section.find_previous('h3').text.strip() if section.find_previous('h3') else prop.capitalize()
            items = [li.text.strip() for li in section.find_all('li')]
            if not items:
                items = [p.text.strip() for p in section.find_all('p')]
            description_sections[section_title] = items

    return {
        'title': title,
        'company': company,
        'location': location,
        'pay': pay,
        'description': description_sections
    }

@app.get("/scrape-jobs")
def scrape_jobs(query: str):
    base_url = "https://www.jobbank.gc.ca"
    search_url = f"{base_url}/jobsearch/jobsearch?searchstring={query.replace(' ', '+')}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    jobs = []
    for job_link in soup.select('a.resultJobItem'):
        job_path = job_link['href']
        full_url = urljoin(base_url, job_path)
        
        try:
            job_details = scrape_job_details(full_url)
            jobs.append(job_details)
        except Exception as e:
            print(f"Error scraping {full_url}: {str(e)}")
            continue
            
    return jobs

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)  # Different port

# scrape Indeed job listings (doesn't work)
'''
@app.get("/scrape-jobs")
def scrape_jobs(query: str):
    url = f"https://ca.indeed.com/jobs?q={query.replace(' ', '+')}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    return [{
        "title": job.select_one(".jobTitle").text.strip(),
        "company": job.select_one(".companyName").text.strip(),
        "description": job.select_one(".job-snippet").text.strip()
    } for job in soup.select(".jobCard")]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)  # Different port
'''