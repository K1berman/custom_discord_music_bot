import os
from dotenv import load_dotenv


load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
PATH_TO_FFMPEG = os.getenv("PATH_TO_FFMPEG")