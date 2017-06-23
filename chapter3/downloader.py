
from urllib.request import Request, urlparse, ProxyHandler, build_opener
from urllib.error import URLError
from chapter3.throttle import Throttle
import random

class Downloader():

    def __init__(self, delay=5, user_agent='wswp', proxies=None, num_retries=1, cache=None):
        self.throttle = Throttle(delay)
        self.user_agent = user_agent
        self.proxies = proxies
        self.num_retries = num_retries
        self.cache = cache


    def __call__(self, url):
        result = None
        if self.cache:
            try:
                result = self.cache[url]
            except KeyError:
                pass
            else:
                if self.num_retries > 0 and result and 500 <= result['code'] < 600:
                    result = None

        if result is None:
            self.throttle.wait(url)
            proxy = random.choice(self.proxies) if self.proxies else None
            headers = {'User-agent': self.user_agent}
            result = self.download(url, headers, proxy, self.num_retries)
            if self.cache:
                #save the result
                self.cache[url] = result
        else:
            print('cached:',url)

        return result['html']


    def download(self, url, headers, proxy, num_retries, data=None):
        print('Downloading:', url)
        request = Request(url, data, headers)
        opener = build_opener()
        if proxy:
            proxy_params = {urlparse(url).scheme: proxy}
            opener.add_handler(ProxyHandler(proxy_params))

        try:
            with opener.open(request) as response:
                html = response.read().decode('utf-8')
                # html = response.read()
                code = response.code
        except URLError as e:
            print('Download error:', e.reason)
            html = ''
            if hasattr(e, 'code'):
                code = e.code
                if num_retries > 0 and 500 <= code < 600:
                    # retry 5XX HTTP errors
                    return self.download(url, headers, proxy, num_retries=-1, data=data)
            else:
                code = None

        return {'html': html, 'code': code}








