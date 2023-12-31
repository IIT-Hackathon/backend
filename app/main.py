from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import user, auth, utility, tax
from dotenv import load_dotenv
import os
load_dotenv()

TEST = os.getenv("TEST")
print("TEST", TEST)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(utility.router)
app.include_router(tax.router)