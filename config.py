import os
from dotenv import load_dotenv


load_dotenv()

if os.name == 'nt':
    if not (PATH_TO_FFMPEG := os.getenv("PATH_TO_FFMPEG")):
        print("Path to FFMPEG not found!")
elif os.name == 'posix':
    if not (PATH_TO_FFMPEG := os.getenv("PATH_TO_FFMPEG")):
        PATH_TO_FFMPEG = "/usr/bin/ffmpeg"
        print(f"The default path to FFMPEG is set: {PATH_TO_FFMPEG}")
else:
    if not (PATH_TO_FFMPEG := os.getenv("PATH_TO_FFMPEG")):
        print("Path to FFMPEG not found!")

if not (DISCORD_TOKEN := os.getenv("DISCORD_TOKEN")):
    print("Discord bot token not found!")


