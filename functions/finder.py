import requests
from bs4 import BeautifulSoup
import json

def get_link_by_trackname(track_name: str) -> str:

    url = f"https://www.youtube.com/results?search_query={track_name}"

    response = requests.get(url)
    if response.status_code != 200:
        return None

    html = response.text

    soup = BeautifulSoup(html, "html.parser")
    try:
        scripts = soup.find_all('script')

        link: str = None

        for script in scripts:
            if 'var ytInitialData' in script.text:
                start_index = script.text.find('var ytInitialData = ') + len('var ytInitialData = ')
                end_index = script.text.find('};', start_index) + 1
                json_data = script.text[start_index:end_index]

                data = json.loads(json_data)

                videos = data['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']

                for i in videos:
                    if i.get('videoRenderer'):
                        link = i['videoRenderer']['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']
                        print(link)
                        break
    except Exception:
        return None

    return f"https://www.youtube.com{link[:link.find('&')]}"
