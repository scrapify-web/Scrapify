from fastapi import FastAPI
from pydantic import BaseModel
from backend.scraper import scrape_site

app = FastAPI(title="SCRAPIFY API")

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
