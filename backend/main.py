import logging
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.routers import auth, project

logger = logging.getLogger(__name__)


origins = [
    "http://127.0.0.1",
    "http://127.0.0.1:5173",
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(project.router)

if os.path.isdir("./dist"):
    app.mount("/", StaticFiles(directory="./dist", html=True), name="static")
else:
    logger.error("No dist folder found. Please run `npm run build` to build the frontend.")
