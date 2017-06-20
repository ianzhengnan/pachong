

from urllib.request import urlopen, Request, build_opener, ProxyHandler
from urllib.error import URLError
from urllib.parse import urlparse
import re

def download(url, user_agent='wswp', num_retries=2):
	print('Downloading:', url)
	headers = {'User-agent': user_agent}
	request = Request(url, headers=headers)
	try:
		# html = urlopen(url).read()
		# html = urlopen(request).read()
		with urlopen(request) as response:
			html = response.read().decode('utf-8')

	except URLError as e:
		print('Download error:', e.reason)
		html = None
		if hasattr(e, 'code') and 500 <= e.code < 600:
			# filter 500+ errors, retry the download
			print('Try again...')
			return download(url, num_retries - 1)
		elif 400 <= e.code < 500:
			print('The page is not exist.')

	return html

def download5(url, user_agent='wswp', proxy=None, num_retries=2):
	print('Downloading:', url)
	headers = {'User-agent': user_agent}
	request = Request(url, headers=headers)
	opener = build_opener()

	if proxy:
		proxy_params = {urlparse(url).scheme: proxy}
		opener.add_handler(ProxyHandler(proxy_params))
	try:
		with opener.open(request) as response:
			html = response.read().decode('utf-8')

	except URLError as e:
		print('Download error:', e.reason)
		html = None
		if hasattr(e, 'code') and 500 <= e.code < 600:
			# filter 500+ errors, retry the download
			print('Try again...')
			return download(url, num_retries - 1)
		elif 400 <= e.code < 500:
			print('The page is not exist.')

	return html


def crawl_sitemap(url):
	#
	sitemap = download(url)
	# extract the sitemap links
	links = re.findall('<loc>(.*?)</loc>', sitemap)
	# download each link
	for link in links:
		html = download(link)
		# print(html)
		print(link)


if __name__ == '__main__':
	html = download5('https://www.youtube.com', proxy = 'proxy.pal.sap.corp:8080')
	print(html)
	# crawl_sitemap('http://weibo.com/sitemap.xml')

