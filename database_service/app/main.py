import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from app.api import diseases, symptoms, user_symptoms
from app.logging_config import setup_logging

setup_logging()
logger = logging.getLogger("app")
app = FastAPI(title="Database Service")

add_pagination(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(symptoms.router, prefix="/api/symptoms", tags=["symptoms"])
app.include_router(diseases.router, prefix="/api/diseases", tags=["diseases"])
app.include_router(user_symptoms.router, prefix="/api/user-symptoms", tags=["user-symptoms"])


@app.get("/api")
async def root():
    logger.debug("Root endpoint")
    return {"message": "Database Service running"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001)
