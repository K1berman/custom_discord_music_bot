from pytube import YouTube


def get_mp3_from_youtube(url: str, path_to_save: str = None, full_file_name:str = "exit.mp3") -> bool:
    try:
        video = YouTube(url = url)
        video = video.streams.get_audio_only()
        if video is None:
            return False
        video.download(output_path = path_to_save, filename = full_file_name)
        return True
    except Exception as error:
        print(f"Ошибка парсинга видео! \n{error}")
        return False