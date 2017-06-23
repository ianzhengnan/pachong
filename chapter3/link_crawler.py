
import re
from collections import deque
from urllib.parse import urlparse, urldefrag, urljoin
from urllib import robotparser
from chapter3.downloader import Downloader


def link_crawler(seed_url, link_regex=None, delay=5, max_depth=-1, max_urls=-1,
				 headers=None, user_agent='wswp', proxies=None, num_retries=1,
				 scrape_callback=None, cache=None, ignore_robots=False):
	"""Crawl from the given seed URL following links matched by link_regex
    """
	# the queue of URL's that still need to be crawled
	crawl_queue = deque([seed_url])
	# the URL's that have been seen and at what depth
	seen = {seed_url: 0}
	# track how many URL's have been downloaded
	num_urls = 0
	rp = get_robots(seed_url)
	headers = headers or {}
	downloader = Downloader(delay=delay, user_agent=user_agent, proxies=proxies, num_retries=num_retries, cache=cache)

	if user_agent:
		headers['user-agent'] = user_agent

	while crawl_queue:
		url = crawl_queue.pop()
		# check url passes robots.txt restrictions
		if ignore_robots or rp.can_fetch(user_agent, url):
			html = downloader(url)
			links = []

			if scrape_callback:
				links.extend(scrape_callback(url, html) or [])
				# scrape_callback(url, html)

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


def get_robots(seed_url):
	"""Initialize robots parser for this domain
    """
	rp = robotparser.RobotFileParser()
	rp.set_url(urljoin(seed_url, '/robots.txt'))
	rp.read()
	return rp


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
