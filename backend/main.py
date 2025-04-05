import logging
import os

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.routers import auth, project, user

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
app.include_router(user.router)


@app.get("/{full_path:path}")
async def serve_spa(full_path: str, request: Request):
    """
    Catch-all route to serve the SPA's index.html for unmatched routes.
    """
    index_path = os.path.join("./dist", "index.html")
    if os.path.isfile(index_path):
        return FileResponse(index_path)
    else:
        return {"error": "index.html not found. Please build the frontend."}


if os.path.isdir("./dist"):
    app.mount("/", StaticFiles(directory="./dist", html=True), name="static")
else:
    logger.error("No dist folder found. Please run `npm run build` to build the frontend.")
