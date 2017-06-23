
from chapter3.link_crawler import link_crawler
from chapter3.mongo_cache import MongoCache
from chapter4.alexa_cb import AlexaCallback

def main():
    scrap_callback = AlexaCallback()
    cache = MongoCache()
    link_crawler(scrap_callback.seed_url, delay=1,
                 num_retries=1, user_agent='GoodCrawel', scrape_callback=scrap_callback ,cache=cache)


if __name__ == '__main__':
    main()