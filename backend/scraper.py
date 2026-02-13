import time, random
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from utils import clean, can_fetch, EMAIL_RE, PHONE_RE

UA = UserAgent()

def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f"user-agent={UA.random}")
    return webdriver.Chrome(options=options)

def scrape_site(url, depth=2, use_js=True):
    visited = set()
    results = []

    def crawl(u, d):
        if d == 0 or u in visited:
            return
        visited.add(u)

        if not can_fetch(u):
            return

        html = None
        try:
            if use_js:
                driver = get_driver()
                driver.get(u)
                time.sleep(random.uniform(2, 4))
                html = driver.page_source
                driver.quit()
            else:
                headers = {"User-Agent": UA.random}
                html = requests.get(u, headers=headers, timeout=10).text
        except:
            return

        soup = BeautifulSoup(html, "lxml")
        text = soup.get_text(" ")

        data = {
            "url": u,
            "title": clean(soup.title.text if soup.title else ""),
            "emails": list(set(EMAIL_RE.findall(text))),
            "phones": list(set(PHONE_RE.findall(text))),
            "links": [],
            "images": []
        }

        for a in soup.find_all("a", href=True):
            link = urljoin(u, a["href"])
            data["links"].append(link)
            if link.startswith("http"):
                crawl(link, d - 1)

        for img in soup.find_all("img", src=True):
            data["images"].append(urljoin(u, img["src"]))

        results.append(data)

    crawl(url, depth)
    return results
