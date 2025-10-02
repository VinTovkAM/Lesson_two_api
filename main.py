from urllib.parse import urlparse
import requests
import os
from dotenv import load_dotenv


def is_shorten_link(TOKEN, url):
    url_api = 'https://api.vk.ru/method/utils.checkLink'
    params = {
        'access_token': TOKEN,
        'url': url,
        'v': 5.199,
    }

    is_shorted_link = False
    response = requests.post(url_api, params=params)
    response.raise_for_status()
    parsed_url = urlparse(url)
    if parsed_url.netloc == 'vk.cc':
        is_shorted_link = True
        url = response.json()['response']['link']
        return url, is_shorted_link

    return url, is_shorted_link


def shorten_link(TOKEN, url):
    url_api = 'https://api.vk.ru/method/utils.getShortLink'
    params = {
        'access_token': TOKEN, 
        'url': url,
        'v': 5.199,
    }

    response = requests.post(url_api, params=params)
    response.raise_for_status()
    short_link = response.json()['response']['short_url']

    return short_link


def count_click(TOKEN, short_link):
    parsed_url = urlparse(short_link)
    url_api = 'https://api.vk.ru/method/utils.getLinkStats'
    params = {
        'access_token': TOKEN,
        'key': parsed_url.path.strip('/'),
        'interval': 'forever',
        'intervals_count': 1,
        'extended': 0,
        'v': 5.199,
    }

    response = requests.post(url_api, params=params)
    response.raise_for_status()
    counter_click = response.json()['response']['stats'][0]['views']

    return counter_click


def main():
    load_dotenv()
    TOKEN = os.getenv('TOKEN')
    url = input('Введите ссылку для сокращения: ')

    try:
        url, is_shorted_link = is_shorten_link(TOKEN, url)
        short_link = shorten_link(TOKEN, url)
        counter_click = count_click(TOKEN, short_link)
    except requests.exceptions.HTTPError as error:
        print(f'Error: {error}')

    if is_shorted_link == False:
        print(f'Сокращённая ссылка: {short_link}')
    else:
        print(f'Кол-во кликов: {counter_click}')


if __name__ == '__main__':
    main()