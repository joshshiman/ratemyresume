# ratemyresume
Helping International Student Stay Competitive
> By: Joshua, Derica, Nikita, and Victoria

## How to Setup

### Frontend

(REFERENCE ONLY) Installing Next.js

`npx create-next-app@latest`

Navigate to frontend folder

`cd frontend`

Running Next.js server

`npm run dev`

### Backend

Navigate to Backend folder

`cd backend`

Create .env file

`touch .env`

Add Google Gemini API key (Obtained from website)

`GOOGLE_API_KEY=[INSERT YOUR KEY HERE]`

Setting up virtual environment

`python -m venv .venv`

Activate virtual environment

- On macOS/Linux:
`source .venv/bin/activate`
- On Windows:
  `.venv\Scripts\activate.bat`

Install requirements (must have PosgreSQL installed)
`pip install -r requirements.txt`

Start Backend server

`uvicorn main:app --reload`
