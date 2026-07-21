from fastapi import FastAPI
from sqlalchemy import text

from app.database import engine

app = FastAPI(
    title="Trip Mitra GO",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Trip Mitra Go is running"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }

@app.get("/database-health")
def database_health():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "database": "connected"
        }

    except Exception as e:
        return {
            "database": "error",
            "message": str(e)
        }