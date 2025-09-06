import os

from dotenv import load_dotenv

# ANSI escape codes for red and reset
RED = "\033[91m"
RESET = "\033[0m"

print("Loading environment variables...")
load_dotenv(override=True)

if "HEALTH_CHECK" in os.environ:
    print("Environment variables loaded.")
else:
    print(RED + "ERROR:  " + RESET + "Could not load environment variables.")

from fastapi import FastAPI

print("Connecting to Mongo...")
from src.utils import dbSetup

dbSetup()
print("Connected to Mongo.")

from src.auth.middleware import JWTAuthMiddleware
from src.views import coupon, signup, template

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(JWTAuthMiddleware)
app.include_router(signup.router)
app.include_router(template.router)
app.include_router(coupon.router)


@app.get("/health")
def read_root() -> dict[str, str]:
    return {"status": "Running"}
