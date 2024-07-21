from pytube import YouTube


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


if __name__ == "__main__":
    print(get_mp3_from_youtube("https://www.youtube.com/watch?v=9I0ZPW0ja_Q&ab_channel=%EB%B6%81%EC%95%85%EA%B4%91%EC%95%BC%E5%8C%97%E5%B2%B3%E7%8B%82%E5%A4%9C"))