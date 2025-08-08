import os

from dotenv import load_dotenv
from fastapi import FastAPI

# ANSI escape codes for red and reset
RED = "\033[91m"
RESET = "\033[0m"

print("Loading environment variables...")
load_dotenv(override=True)

if "HEALTH_CHECK" in os.environ:
    print("Environment variables loaded.")
else:
    print(RED + "ERROR:  " + RESET + "Could not load environment variables.")

print("Connecting to Mongo...")
from src.utils import dbSetup

dbSetup()
print("Connected to Mongo.")

app = FastAPI()


@app.get("/health")
def read_root():
    return {"status": "Running"}
