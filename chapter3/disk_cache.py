
import os
import re
import pickle
import zlib
import shutil
from urllib.parse import urlsplit
from link_crawler import link_crawler
from datetime import datetime, timedelta

class DiskCache():

    def __init__(self, cache_dir='cache', expires=timedelta(days=30), compress=True):
        self.cache_dir = cache_dir
        self.expires = expires
        self.compress = compress

    def url_to_path(self, url):

        components = urlsplit(url)
        # append index.html to empty paths
        path = components.path
        if not path:
            path = '/index.html'
        elif path.endswith('/'):
            path += 'index.html'
        filename = components.netloc + path + components.query
        # replace invalid characters
        filename = re.sub('[^/0-9a-zA-Z\-.,;_ ]', '_', filename)
        # restrict maximum number of characters
        filename = '/'.join(segment[:255] for segment in filename.split('/'))

        return os.path.join(self.cache_dir, filename)

    def __getitem__(self, url):
        """
        Load data from disk for this URL
        :param url:
        :return:
        """
        path = self.url_to_path(url)
        if os.path.exists(path):
            with open(path, 'rb') as fp:
                data = fp.read()
                if self.compress:
                    data = zlib.decompress(data)
                result, timestamp = pickle.loads(data)
                if self.has_expired(timestamp):
                    raise KeyError(url + 'has expired')
                return result
        else:
            # URL has not yet been cached
            raise KeyError(url + ' does not exist')

    def __setitem__(self, url, result):
            """
            save data to disk for the url
            :param url:
            :param result:
            :return:
            """
            path = self.url_to_path(url)
            folder = os.path.dirname(path)
            if not os.path.exists(folder):
                os.makedirs(folder)

            data = pickle.dumps((result, datetime.utcnow()))
            if self.compress:
                data = zlib.compress(data)
            with open(path, 'wb') as fp:
                fp.write(data)

    def __delitem__(self, url):
        path = self._key_path(url)
        try:
            os.remove(path)
            os.removedirs(os.path.dirname(path))
        except OSError:
            pass

    def has_expired(self, timestamp):
        return datetime.utcnow() > timestamp + self.expires

    def clear(self):
        '''
        remove all cached values
        :return:
        '''
        if os.path.exists(self.cache_dir):
            shutil.rmtree(self.cache_dir)

if __name__ == '__main__':
    link_crawler('http://example.webscraping.com', r'[0-9a-zA-Z./:]*/(index|view)/[0-9a-zA-Z./:]*', delay=1,
                 num_retries=1, user_agent='BadCrawel', cache=DiskCache())
    # DiskCache().clear()