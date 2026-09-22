import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("HF_TOKEN")

if token:
    print("HF token loaded successfully")
    print("Token starts with:", token[:7])
else:
    print("HF_TOKEN was not found")