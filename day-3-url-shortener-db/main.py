import os
import random
import string

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session

import models
from database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

app = FastAPI(title="URL Shortener v2")


class URLRequest(BaseModel):
    url: HttpUrl


def generate_code(length: int = 6) -> str:
    chars = string.ascii_letters + string.digits
    return "".join(random.choices(chars, k=length))


@app.get("/")
def health(db: Session = Depends(get_db)):
    total = db.query(models.URL).count()
    return {"status": "ok", "total_urls": total}


@app.post("/shorten")
def shorten(payload: URLRequest, db: Session = Depends(get_db)):
    code = generate_code()
    while db.query(models.URL).filter_by(code=code).first():
        code = generate_code()

    entry = models.URL(code=code, original_url=str(payload.url))
    db.add(entry)
    db.commit()
    return {"short_code": code, "short_url": f"{BASE_URL}/{code}"}


@app.get("/stats/{code}")
def stats(code: str, db: Session = Depends(get_db)):
    entry = db.query(models.URL).filter_by(code=code).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Short code not found")
    return {
        "code": entry.code,
        "original_url": entry.original_url,
        "visits": entry.visits,
        "created_at": entry.created_at,
    }


@app.get("/{code}")
def redirect(code: str, db: Session = Depends(get_db)):
    entry = db.query(models.URL).filter_by(code=code).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Short code not found")
    entry.visits += 1
    db.commit()
    return RedirectResponse(entry.original_url)