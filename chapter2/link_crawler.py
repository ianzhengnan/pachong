
import re
import time
from datetime import datetime
from collections import deque
from urllib.request import urlopen, Request, build_opener, ProxyHandler
from urllib.error import URLError
from urllib.parse import urlparse, urldefrag, urljoin
from urllib import robotparser


def link_crawler(seed_url, link_regex=None, delay=5, max_depth=-1, max_urls=-1, headers=None, user_agent='wswp', proxy=None, num_retries=1, scrape_callback=None):
	"""Crawl from the given seed URL following links matched by link_regex
    """
    # the queue of URL's that still need to be crawled
	crawl_queue = deque([seed_url])
	# the URL's that have been seen and at what depth
	seen = {seed_url: 0}
	# track how many URL's have been downloaded
	num_urls = 0
	rp = get_robots(seed_url)
	throttle = Throttle(delay)
	headers = headers or {}

	if user_agent:
		headers['user-agent'] = user_agent

	while crawl_queue:
		url = crawl_queue.pop()
		# check url passes robots.txt restrictions
		if rp.can_fetch(user_agent, url):
			throttle.wait(url)
			html = download(url, headers, proxy=proxy, num_retries=num_retries)
			links = []

			if scrape_callback:
				# links.extend(scrape_callback(url, html) or [])
				scrape_callback(url, html)

			depth = seen[url]
			if depth != max_depth:
				# can still crawl further
				if link_regex:
				# filter for links matching our regular expression
					links.extend(link for link in get_links(
					    html) if re.match(link_regex, link))

				for link in links:
					link = normalize(seed_url, link)
					# check whether already crawled this link
					if link not in seen:
						seen[link] = depth + 1
						# check link is within same domain
						if same_domain(seed_url, link):
							# success! add this new link to queue
							crawl_queue.append(link)

			# check whether have reached downloaded maximum
			num_urls += 1
			if num_urls == max_urls:
				break
		else:
			print('Blocked by robots.txt:', url)


class Throttle():
	"""Throttle downloading by sleeping between requests to same domain
    """

	def __init__(self, delay):
    	# amount of delay between downloads for each domain
		self.delay = delay
		# timestamp of when a domain was last accessed
		self.domains = {}

	def wait(self, url):
		domain = urlparse(url).netloc
		last_accessed = self.domains.get(domain) or datetime.now()

		if self.delay > 0 and last_accessed is not None:
			sleep_secs = self.delay - (datetime.now() - last_accessed).seconds
			if sleep_secs > 0:
				time.sleep(sleep_secs)
			self.domains[domain] = datetime.now()


def get_robots(seed_url):
	"""Initialize robots parser for this domain
    """
	rp = robotparser.RobotFileParser()
	rp.set_url(urljoin(seed_url, '/robots.txt'))
	rp.read()
	return rp


def download(url, headers, proxy, num_retries, data=None):
	print('Downloading:', url)
	request = Request(url, data, headers)
	opener = build_opener()
	if proxy:
		proxy_params = {urlparse(url).scheme: proxy}
		opener.add_handler(ProxyHandler(proxy_params))

	try:
		with opener.open(request) as response:
			html = response.read().decode('utf-8')
			code = response.code
	except URLError as e:
		print('Download error:', e.reason)
		html = ''
		if hasattr(e, 'code'):
			code = e.code
			if num_retries > 0 and 500 <= code < 600:
				# retry 5XX HTTP errors
				return download(url, headers, proxy, num_retries=-1, data=data)
		else:
			code = None

	return html


def normalize(seed_url, link):
	"""Normalize this URL by removing hash and adding domain
    """
	link, _ = urldefrag(link)
	return urljoin(seed_url, link)


def same_domain(url1, url2):
	"""Return True if both URL's belong to same domain
    """
	return urlparse(url1).netloc == urlparse(url2).netloc
				

def get_links(html):
	"""Return a list of links from html 
    """
    # a regular expression to extract all links from the webpage
	webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
	return webpage_regex.findall(html)


if __name__ == '__main__':
	link_crawler('http://example.webscraping.com', r'[0-9a-zA-Z./:]*/(index|view)/[0-9a-zA-Z./:]*', delay=1, num_retries=1, user_agent='BadCrawel')
	# link_crawler('http://example.webscraping.com', r'[0-9a-zA-Z./:]*/(index|view)/[0-9a-zA-Z./:]*', delay=3, num_retries=1, max_depth=1, user_agent='GoodCrawel')
