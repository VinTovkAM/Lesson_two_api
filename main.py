from urllib.parse import urlparse
import requests
import os
from dotenv import load_dotenv


def get_shorten_link(token, url):
    url_api = 'https://api.vk.ru/method/utils.getShortLink'
    params = {
        'access_token': token,
        'url': url,
        'v': 5.199,
    }

    response = requests.post(url_api, params=params)
    response.raise_for_status()

    return response.json()['response']['short_url']


def get_count_click(token, short_link):
    parsed_url = urlparse(short_link)
    url_api = 'https://api.vk.ru/method/utils.getLinkStats'
    params = {
        'access_token': token,
        'key': parsed_url.path.strip('/'),
        'interval': 'forever',
        'intervals_count': 1,
        'extended': 0,
        'v': 5.199,
    }

    response = requests.post(url_api, params=params)
    response.raise_for_status()
    
    return response.json()['response']['stats'][0]['views']


def is_shorten_link(token, url):
    parsed_url = urlparse(url)
    url_api = 'https://api.vk.ru/method/utils.checkLink'
    params = {
        'access_token': token,
        'url': url,
        'v': 5.199,
    }

    response = requests.post(url_api, params=params)
    response.raise_for_status()

    if response.json()["response"]["status"] == "not_banned":
        if parsed_url.netloc == 'vk.cc':
            return True
        else:
            return False


def main():
    load_dotenv()
    token = os.getenv('TOKEN')
    url = input('Введите ссылку для сокращения: ')
    try:
        if not is_shorten_link(token, url):
            short_url = get_shorten_link(token, url)
            print(f"Сокращённая ссылка: {short_url}")
        else:
            print(f"Количество кликов по ссылке: {get_count_click(token, url)}")
    except requests.exceptions.HTTPError as error:
        print(f'Error: {error}')


if __name__ == '__main__':
    main()