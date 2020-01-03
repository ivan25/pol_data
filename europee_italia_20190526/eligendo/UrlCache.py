import time, json
from datetime import datetime

class UrlCache:
	def __init__(self, min_time):
		self.dict_urls = {}
		self.min_time = min_time
		
		self.passthrough = [
			"https://eleapi.interno.gov.it/siel/PX/votaultimi/TE/01",
			"https://eleapi.interno.gov.it/siel/PX/scruultimiEI/TE/01",
			"https://eleapi.interno.gov.it/siel/PX/votanti/TE/01",
			"https://eleapi.interno.gov.it/siel/PX/scrutiniEI/TE/01"
		]
		
	def get_url(self, url):
		if url in self.passthrough:
			return True
	
		if url not in self.dict_urls:
			self.dict_urls[url] = datetime.now().timestamp()
			return True
			
		if datetime.now().timestamp() - self.dict_urls[url] > self.min_time:
			self.dict_urls[url] = datetime.now().timestamp()
			return True
			
		return False		
