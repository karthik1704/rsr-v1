from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, users

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

app.include_router(users.router)
app.include_router(auth.router)
