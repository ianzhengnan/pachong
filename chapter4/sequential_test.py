
from chapter3.link_crawler import link_crawler
from chapter3.mongo_cache import MongoCache
from chapter4.alexa_cb import AlexaCallback
from chapter3.downloader import Downloader

def main():
    scrap_callback = AlexaCallback()
    cache = MongoCache()
    links = list(scrap_callback())

    downloader = Downloader(cache=cache)

    while links:
        url = links.pop()
        html = downloader(url)
        print(url)


if __name__ == '__main__':
    main()