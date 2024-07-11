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
    print(get_mp3_from_youtube("https://www.youtube.com/watch?v=p0NueP55kjs&ab_channel=%D0%90%D0%BD%D0%B4%D1%80%D0%B5%D0%B9%D0%98%D0%B2%D0%B0%D0%BD%D0%BE%D0%B2%7CPython"))