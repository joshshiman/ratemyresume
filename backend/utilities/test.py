import requests

response = requests.get("http://localhost:8001/jobs")
print(response.json())