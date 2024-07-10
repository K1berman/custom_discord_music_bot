from pytube import YouTube
import requests
from bs4 import BeautifulSoup

def get_mp3_from_youtube(url: str, path_to_save: str = None, full_file_name:str = "exit.mp3") -> bool:
    try:
        video = YouTube(url = url)
        audio = video.streams.filter(only_audio=True).order_by('abr').desc().first()
        if audio is None:
            return False
        audio.download(output_path = path_to_save, filename = full_file_name)
        return True
    except Exception as error:
        print(f"Ошибка парсинга видео! \n{error}")
        return False


