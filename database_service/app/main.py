import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.logging_config import setup_logging
setup_logging()
import logging

logger = logging.getLogger("app")

from app.api import symptoms, user_symptoms

app = FastAPI(title="Database Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(symptoms.router, prefix="/symptoms", tags=["symptoms"])
app.include_router(user_symptoms.router, prefix="/user-symptoms",
                   tags=["user-symptoms"])

@app.get("/")
async def read_root():
    logger.debug("Обработка запроса на эндпоинт '/'")
    return {"message": "Database Service работает!"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
