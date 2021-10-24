from os import environ as env
from dotenv import load_dotenv

load_dotenv()

GITHUB_ACCESS_TOKEN = env.get("GITHUB_ACCESS_TOKEN")
NV_URL = env.get("NV_URL")
NV_CLIENT_ID = env.get("NV_CLIENT_ID")
NV_CLIENT_SECRET = env.get("NV_CLIENT_SECRET")
GITHUB_REPO = env.get("GITHUB_REPO")
