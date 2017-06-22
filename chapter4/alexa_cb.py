
import csv
from io import StringIO
from zipfile import ZipFile
from chapter3.mongo_cache import MongoCache

class AlexaCallback():

    def __init__(self, max_urls=1000):
        self.max_urls = max_urls
        self.seed_url = 'http://s3.amazonaws.com/alexa-static/top-1m.csv.zip'

    def __call__(self, url, html):
        if url == self.seed_url:
            urls = []
            cache = MongoCache()
            with open(html) as zf:
                csv_filename = zf.name #zf.namelist()[0]
                for _, website in csv.reader(zf):
                    if 'http://' + website not in cache:
                        urls.append('http://' + website)
                        if len(urls) == self.max_urls:
                            break

            return urls


if __name__ == '__main__':
    result = AlexaCallback()('http://s3.amazonaws.com/alexa-static/top-1m.csv.zip', '/home/vagrant/Downloads/top-1m.csv')
    print(result)