# ⚡ LinkTrim - URL Shortener API

A lightweight, fast URL shortening microservice with custom aliases and click tracking analytics built with FastAPI.

## ✨ Features

- **Fast URL Shortening:** Generates deterministic SHA-256 short codes.
- **Custom Aliases:** Support for optional custom vanity slugs.
- **Click Analytics:** Tracks total clicks and timestamp of the last access.
- **Auto-generated Documentation:** Interactive Swagger UI out of the box.

## 🚀 Quickstart

```bash
git clone https://github.com/malikrihanpasha2004-cloud/my-first-project-.git
cd my-first-project-
pip install -r requirements.txt
uvicorn main:app --reload
