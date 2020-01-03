import time, json

from eligendo import Downloader, DownloaderAffluenza, DownloaderScrutini, UrlCache
from eligendo.utils import log, current_time

cache1 = UrlCache.UrlCache(60)
cache2 = UrlCache.UrlCache(60)

dw1 = DownloaderAffluenza.DownloaderAffluenza(
	base_folder = '~/Scrivania/download_eligendo',
	base_headers = [
		['Host', 'eleapi.interno.gov.it'], ['Accept-Language', 'it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3'],
		['User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0'],
		['Accept', 'application/json, text/javascript, */*; q=0.01'], ['Pragma', 'no-cache'],
		['DNT', '1'], ['Connection', 'keep-alive'], ['Content-Type', 'application/json'],
		['Origin', 'https://elezioni.interno.gov.it'], ['Accept-Encoding', 'gzip, deflate, br'],
		['Cache-Control', 'no-cache']
	],
	cache=cache1
)

dw2 = DownloaderScrutini.DownloaderScrutini(
	base_folder = '~/Scrivania/download_eligendo',
	base_headers = [
		['Host', 'eleapi.interno.gov.it'], ['Accept-Language', 'it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3'],
		['User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0'],
		['Accept', 'application/json, text/javascript, */*; q=0.01'], ['Pragma', 'no-cache'],
		['DNT', '1'], ['Connection', 'keep-alive'], ['Content-Type', 'application/json'],
		['Origin', 'https://elezioni.interno.gov.it'], ['Accept-Encoding', 'gzip, deflate, br'],
		['Cache-Control', 'no-cache']
	],
	cache=cache2
)

dw1.carica_codici_comuni('europee_territoriale_italia.json')
dw2.carica_codici_comuni('europee_territoriale_italia.json')

# imposto gli url per i download
#	1) url per gli enti ultimi pervenuti, votanti e scrutini
with open('urls.json', 'r') as f: dict_urls = json.load(f)

dw1.set_urls('ultimi_ep_votanti', dict_urls['ultimi_ep_votanti'])
dw1.set_urls('votanti_italia', dict_urls['votanti_italia'])

dw2.set_urls('ultimi_ep_scrutini', dict_urls['ultimi_ep_scrutini'])
dw2.set_urls('scrutini_italia', dict_urls['scrutini_italia'])

# ##############################################################################

# ciclo per lo scarico dei dati dell'affluenza
while True:

	log('{} : INIZIO CICLO -----'.format(current_time()), style='headline')

	#dw1.scarica('votanti_italia')
	#dw1.scarica('ultimi_ep_votanti')
	
	dw2.scarica('scrutini_italia')
	dw2.scarica('ultimi_ep_scrutini')	
	
	#ultimi_ep_votanti = dw1.calcola_enti_pervenuti('ultimi_ep_votanti')
	#url_enti_superiori_votanti = dw1.calcola_urls_enti_superiori(ultimi_ep_votanti)
	#dw1.scarica_files(url_enti_superiori_votanti)
	
	ultimi_ep_scrutini = dw2.calcola_enti_pervenuti('ultimi_ep_scrutini')
	url_enti_superiori_scrutini = dw2.calcola_urls_enti_superiori(ultimi_ep_scrutini)
	dw2.scarica_files(url_enti_superiori_scrutini)	
	
	time.sleep(10)
