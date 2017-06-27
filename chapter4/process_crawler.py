
import time
import threading
import multiprocessing
from chapter3.downloader import Downloader
from chapter3.mongo_cache import MongoCache
from chapter4.alexa_cb import AlexaCallback
from chapter4.mongo_queue import MongoQueue

SLEEP_TIME = 1

def threaded_crawler(cache=None, max_threads=10):
    """
    Crawl this website in mutiple thread
    :param cache:
    :return:
    """
    scrap_callback = AlexaCallback()

    links = list(scrap_callback())

    crawl_queue = MongoQueue()
    crawl_queue.clear()
    for link in links:
        crawl_queue.push(link)

    cache = MongoCache()
    downloader = Downloader(cache=cache)

    def process_queue():
        while True:
            try:
                url = crawl_queue.pop()
            except IndexError:
                break
            else:
                html = downloader(url)
                crawl_queue.complete(url)

    # wait for all download threads to finish
    threads = []
    while threads or crawl_queue:
        # the crawl is still active
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)
        while len(threads) < max_threads and crawl_queue.peek():
            # can start some more threads
            thread = threading.Thread(target=process_queue)
            thread.setDaemon(True)
            thread.start()
            threads.append(thread)

        # all threads have been processed
        # sleep temporarily so CPU can focus execution on other threads
        time.sleep(SLEEP_TIME)


def process_crawler(**kwargs):
    num_cpus = multiprocessing.cpu_count()
    print('Starting {} processes'.format(num_cpus))
    processes = []
    for i in range(num_cpus):
        p = multiprocessing.Process(target=threaded_crawler, args=(None,), kwargs=kwargs)
        p.start()
        processes.append(p)

    # wait for processes to complete
    for p in processes:
        p.join()


if __name__ == '__main__':
    process_crawler(max_threads=20)

