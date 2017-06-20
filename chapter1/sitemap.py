
import re
from urllib.parse import urljoin
from first import download


def link_crawler(seed_url, link_regex):
	
	crawl_queue = [seed_url]
	seen = set(crawl_queue)
	while crawl_queue:
		url = crawl_queue.pop()
		html = download(url)
		for link in get_links(html):
			if re.match(link_regex, link):
				link = urljoin(seed_url, link)
				if link not in seen:
					seen.add(link)
					crawl_queue.append(link)


def get_links(html):
	
	webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
	# print(webpage_regex)
	return webpage_regex.findall(html)

if __name__ == '__main__':
	html = link_crawler("http://startbootstrap.com", '/template-overviews/')
	print(html)
