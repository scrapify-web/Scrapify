import re
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
PHONE_RE = re.compile(r"\+?\d[\d\s\-()]{7,}")

def clean(text):
    return " ".join(text.split()) if text else ""

def can_fetch(url):
    rp = RobotFileParser()
    parsed = urlparse(url)
    rp.set_url(f"{parsed.scheme}://{parsed.netloc}/robots.txt")
    try:
        rp.read()
        return rp.can_fetch("*", url)
    except:
        return True
