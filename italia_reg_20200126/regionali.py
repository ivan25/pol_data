import time, json, os
import random

from eligendo import Downloader, DownloaderAffluenza, DownloaderScrutini, UrlCache
from eligendo.utils import log, current_time

cache1 = UrlCache.UrlCache(10)
cache2 = UrlCache.UrlCache(20)

dw1 = DownloaderAffluenza.DownloaderAffluenza(
	base_folder = '/home/ivan/Scrivania/eligendo_reg_20200126',
	base_headers = [
		['Host', 'eleapi.interno.gov.it'], ['Accept-Language', 'it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3'],
		['User-Agent', ''],
		['Accept', 'application/json, text/javascript, */*; q=0.01'], ['Pragma', 'no-cache'],
		['DNT', '1'], ['Connection', 'keep-alive'], ['Content-Type', 'application/json'],
		['Origin', 'https://elezioni.interno.gov.it'], ['Accept-Encoding', 'gzip, deflate, br'],
		['Cache-Control', 'no-cache']
	],
	cache=cache1
)

dw2 = DownloaderScrutini.DownloaderScrutini(
	base_folder = '/home/ivan/Scrivania/eligendo_reg_20200126',
	base_headers = [
		['Host', 'eleapi.interno.gov.it'], ['Accept-Language', 'it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3'],
		['User-Agent', ''],
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
with open('urls.json', 'r') as f: dict_urls = json.load(f)

dw1.set_urls('ultimi_ep_votanti', dict_urls['ultimi_ep_votanti'])
dw2.set_urls('ultimi_ep_scrutini', dict_urls['ultimi_ep_scrutini'])

dw1.set_urls('votanti_er', dict_urls['votanti_er'])
dw1.set_urls('votanti_calabria', dict_urls['votanti_calabria'])
dw2.set_urls('scrutini_er', dict_urls['scrutini_er'])
dw2.set_urls('scrutini_calabria', dict_urls['scrutini_calabria'])

# ##############################################################################

n = 0

# ciclo per lo scarico dei dati dell'affluenza
while True:

	log('{} : INIZIO CICLO -----'.format(current_time()), style='headline')

	# --------------------------------------------------------------------------
	#      V          O          T          A          N          T        I
	# --------------------------------------------------------------------------
	
	#dw1.scarica('ultimi_ep_votanti')
	
	#ultimi_ep_votanti = dw1.calcola_enti_pervenuti('ultimi_ep_votanti')
	#url_enti_superiori_votanti = dw1.calcola_urls_enti_superiori(ultimi_ep_votanti)
	#dw1.scarica_files(url_enti_superiori_votanti)
	
	# --------------------------------------------------------------------------
	#      S        C         R          U       T        I        N        I
	# --------------------------------------------------------------------------

	# guardo a che punto dello scrutinio sono, in modo che quando arriva alla fine termina
	# e posso lasciare il pc acceso per scaricare
	ultimo_file_scrutini_er = sorted([file_i for file_i in os.listdir('scrutini') if file_i.startswith('scrutini_RE_08_-')])[-1]
	ultimo_file_scrutini_cal = sorted([file_i for file_i in os.listdir('scrutini') if file_i.startswith('scrutini_RE_18_-')])[-1]
	
	with open(os.path.join('scrutini', ultimo_file_scrutini_er), 'r') as f: data_ultimo_scrutini_er = json.load(f)
	with open(os.path.join('scrutini', ultimo_file_scrutini_cal), 'r') as f: data_ultimo_scrutini_cal = json.load(f)
	
	min_sz_er = min(data_ultimo_scrutini_er['int']['sz_cons'], data_ultimo_scrutini_er['int']['sz_pres'])
	min_sz_cal = min(data_ultimo_scrutini_cal['int']['sz_cons'], data_ultimo_scrutini_cal['int']['sz_pres'])
	
	if (min_sz_er < data_ultimo_scrutini_er['int']['sz_tot']) or \
			(min_sz_cal < ultimo_file_scrutini_cal['int']['sz_tot']) or \
			random.randint(0, 100) <= 5:
		
		dw2.scarica('ultimi_ep_scrutini')
		
		ultimi_ep_scrutini = dw2.calcola_enti_pervenuti('ultimi_ep_scrutini')
		url_enti_superiori_scrutini = dw2.calcola_urls_enti_superiori(ultimi_ep_scrutini)
		dw2.scarica_files(url_enti_superiori_scrutini)
		
		if len(list(ultimi_ep_scrutini)) == 0: n += 1
		else: n = 0
	
	# --------------------------------------------------------------------------
	#      S             L               E                E              P
	# --------------------------------------------------------------------------
	
	time.sleep(30 + n)
