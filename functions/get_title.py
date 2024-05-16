from pytube import YouTube


def get_mp3_from_youtube(url: str) -> str | None:
    try:
        video = YouTube(url = url)
        title = video.title
        if title is None:
            return False
        return title
    except Exception as error:
        print(f"Ошибка парсинга названия! \n{error}")
        return False