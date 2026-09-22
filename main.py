import hashlib
from datetime import datetime
from typing import Dict, Optional
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl

app = FastAPI(
    title="LinkTrim - URL Shortener API",
    description="A high-performance URL shortener with analytics.",
    version="1.0.0"
)

url_store: Dict[str, dict] = {}


class URLCreateRequest(BaseModel):
    url: HttpUrl
    custom_code: Optional[str] = None


class URLResponse(BaseModel):
    short_code: str
    short_url: str
    original_url: str
    created_at: str


class AnalyticsResponse(BaseModel):
    short_code: str
    original_url: str
    clicks: int
    created_at: str
    last_accessed: Optional[str] = None


def generate_short_code(url: str, length: int = 6) -> str:
    hash_object = hashlib.sha256(url.encode())
    return hash_object.hexdigest()[:length]


@app.post("/shorten", response_model=URLResponse, status_code=status.HTTP_201_CREATED)
def shorten_url(payload: URLCreateRequest):
    original_url_str = str(payload.url)

    if payload.custom_code:
        code = payload.custom_code.strip()
        if code in url_store:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Custom code already taken."
            )
    else:
        code = generate_short_code(original_url_str)
        counter = 1
        base_code = code
        while code in url_store and url_store[code]["original_url"] != original_url_str:
            code = f"{base_code}{counter}"
            counter += 1

    if code not in url_store:
        url_store[code] = {
            "original_url": original_url_str,
            "clicks": 0,
            "created_at": datetime.utcnow().isoformat(),
            "last_accessed": None,
        }

    return URLResponse(
        short_code=code,
        short_url=f"http://127.0.0.1:8000/{code}",
        original_url=original_url_str,
        created_at=url_store[code]["created_at"]
    )


@app.get("/{short_code}")
def redirect_to_url(short_code: str):
    record = url_store.get(short_code)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Short URL not found.")

    record["clicks"] += 1
    record["last_accessed"] = datetime.utcnow().isoformat()

    return RedirectResponse(url=record["original_url"], status_code=status.HTTP_307_TEMPORARY_REDIRECT)


@app.get("/analytics/{short_code}", response_model=AnalyticsResponse)
def get_analytics(short_code: str):
    record = url_store.get(short_code)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Short code not found.")

    return AnalyticsResponse(
        short_code=short_code,
        original_url=record["original_url"],
        clicks=record["clicks"],
        created_at=record["created_at"],
        last_accessed=record["last_accessed"]
    )
