import time, json, os

from eligendo import Downloader, DownloaderAffluenza, DownloaderScrutini, UrlCache
from eligendo.utils import log, current_time

cache1 = UrlCache.UrlCache(10)
cache2 = UrlCache.UrlCache(10)

dw1 = DownloaderAffluenza.DownloaderAffluenza(
	base_folder = '~/Scrivania/eligendo_umbria',
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
	base_folder = '~/Scrivania/eligendo_umbria',
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

dw1.carica_codici_comuni('regionali_territoriale_italia.json')
dw2.carica_codici_comuni('regionali_territoriale_italia.json')

# imposto gli url per i download
#	1) url per gli enti ultimi pervenuti, votanti e scrutini
with open('urls.json', 'r') as f: dict_urls = json.load(f)

dw1.set_urls('votanti_umbria', dict_urls['votanti_umbria'])
dw1.set_urls('votanti_perugia', dict_urls['votanti_perugia'])
dw1.set_urls('votanti_terni', dict_urls['votanti_terni'])

dw2.set_urls('ultimi_ep_scrutini', dict_urls['ultimi_ep_scrutini'])
dw2.set_urls('scrutini_umbria', dict_urls['scrutini_umbria'])
dw2.set_urls('scrutini_perugia', dict_urls['scrutini_perugia'])
dw2.set_urls('scrutini_terni', dict_urls['scrutini_terni'])

# ##############################################################################

# ciclo per lo scarico dei dati dell'affluenza
while True:

	log('{} : INIZIO CICLO -----'.format(current_time()), style='headline')

	#dw1.scarica('votanti_umbria')
	#dw1.scarica('votanti_perugia')
	#dw1.scarica('votanti_terni')
	
	##
	
	# guardo a che punto dello scrutinio sono, in modo che quando arriva alla fine termina
	# e posso lasciare il pc acceso per scaricare
	ultimo_scrutini = sorted(
		[file_i for file_i in os.listdir('~/Scrivania/eligendo_umbria/scrutini/') if 'scrutini_UMBRIA' in file_i],
    	key=lambda d: '-'.join(d.split('-')[1:3])
	)[-1]
	ultimo_scrutini = os.path.join('~/Scrivania/eligendo_umbria/scrutini/', ultimo_scrutini)
	
	with open(ultimo_scrutini, 'r') as f: dict_ultimo = json.load(f)
		
	log(f"{dict_ultimo['int']['sz_pres']}, {dict_ultimo['int']['sz_cons']} \t {dict_ultimo['int']['sz_tot']}", style='headline')
		
	if min(dict_ultimo['int']['sz_pres'], dict_ultimo['int']['sz_cons']) < dict_ultimo['int']['sz_tot']:
	
		dw2.scarica('ultimi_ep_scrutini')
		
		ultimi_ep_scrutini = dw2.calcola_enti_pervenuti('ultimi_ep_scrutini')
		url_enti_superiori_scrutini = dw2.calcola_urls_enti_superiori(ultimi_ep_scrutini)
		dw2.scarica_files(url_enti_superiori_scrutini)
		
		if len(ultimi_ep_scrutini) > 0:
			dw2.scarica('scrutini_umbria')
			dw2.scarica('scrutini_perugia')
			dw2.scarica('scrutini_terni')
	
	time.sleep(100)
