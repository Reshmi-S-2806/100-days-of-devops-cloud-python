import random
import string

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl

app = FastAPI(title="URL Shortener")


url_db: dict[str, str] = {}


class URLRequest(BaseModel):
    url: HttpUrl


def generate_code(length: int = 6) -> str:
    chars = string.ascii_letters + string.digits
    return "".join(random.choices(chars, k=length))


@app.get("/")
def health():
    return {"status": "ok", "total_urls": len(url_db)}


@app.post("/shorten")
def shorten(payload: URLRequest):
    code = generate_code()
    while code in url_db:
        code = generate_code()
    url_db[code] = str(payload.url)
    return {"short_code": code, "short_url": f"http://localhost:8000/{code}"}


@app.get("/{code}")
def redirect(code: str):
    if code not in url_db:
        raise HTTPException(status_code=404, detail="Short code not found")
    return RedirectResponse(url_db[code])