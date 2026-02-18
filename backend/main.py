from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from scraper import scrape_site

app = FastAPI(title="SCRAPIFY API")

# ✅ Strong CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://scrapify-frontend.onrender.com"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScrapeRequest(BaseModel):
    url: str
    depth: int = 2
    use_js: bool = True

@app.get("/")
def root():
    return {"status": "SCRAPIFY backend running 🚀"}

@app.post("/scrape")
def scrape(req: ScrapeRequest):
    data = scrape_site(req.url, req.depth, req.use_js)
    return {"pages": data}
