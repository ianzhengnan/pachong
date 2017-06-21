
import time
from urllib.parse import urlparse
from datetime import datetime


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