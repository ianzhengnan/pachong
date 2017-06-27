
import csv
from io import StringIO
from zipfile import ZipFile
from chapter3.mongo_cache import MongoCache

class AlexaCallback():

    def __init__(self, max_urls=1000):
        self.max_urls = max_urls
        self.seed_url = 'http://s3.amazonaws.com/alexa-static/top-1m.csv.zip'
        self.csv_file = '/home/vagrant/Downloads/top-1m.csv'

    def __call__(self):

        urls = []
        # cache = MongoCache()
        with open(self.csv_file, 'r') as zf:
            for _, website in csv.reader(zf):
                # if 'http://' + website not in cache:
                urls.append('http://' + website)
                if len(urls) == self.max_urls:
                    break

        return urls


if __name__ == '__main__':
    result = AlexaCallback()()
    print(result)