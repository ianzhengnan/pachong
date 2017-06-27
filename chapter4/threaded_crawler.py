
import time
import threading
from chapter3.downloader import Downloader
from chapter3.mongo_cache import MongoCache
from chapter4.alexa_cb import AlexaCallback

SLEEP_TIME = 1

def threaded_crawler(cache=None, max_threads=10):
    """
    Crawl this website in mutiple thread
    :param cache:
    :return:
    """
    scrap_callback = AlexaCallback()

    links = list(scrap_callback())
    cache = MongoCache()
    downloader = Downloader(cache=cache)

    def process_queue():
        while True:
            try:
                url = links.pop()
            except IndexError:
                break
            else:
                html = downloader(url)

    # wait for all download threads to finish
    threads = []
    while threads or links:
        # the crawl is still active
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)
        while len(threads) < max_threads and links:
            # can start some more threads
            thread = threading.Thread(target=process_queue)
            thread.setDaemon(True)
            thread.start()
            threads.append(thread)

        # all threads have been processed
        # sleep temporarily so CPU can focus execution on other threads
        time.sleep(SLEEP_TIME)


if __name__ == '__main__':
    threaded_crawler()

