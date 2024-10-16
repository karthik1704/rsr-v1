from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routers import auth, resume, stripe_payment, users

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://3.110.169.239:3002",
    "http://3.110.169.239:3000",
    "http://3.110.169.239",
    "http://13.201.194.87",
    # "http://rsrglobalresumebuilder.com",
    "https://www.rsrglobalresumebuilder.com",
    "https://rsrglobalresumebuilder.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# serving images

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Serve the `uploads/` directory at the `/static` path
app.mount("/static", StaticFiles(directory=UPLOAD_DIR), name="static")


app.include_router(users.router)
app.include_router(auth.router)
app.include_router(resume.router)
app.include_router(stripe_payment.router)

