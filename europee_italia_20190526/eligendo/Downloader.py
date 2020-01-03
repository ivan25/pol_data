import requests as req
import json, os
from datetime import datetime

from .utils import log, scarica_file, current_time, codici_enti

class Downloader:
	def __init__(self, base_folder, base_headers, cache=None):
		self.dict_url = {}
		self.base_folder = base_folder
		self.base_headers = base_headers
		self.cache = cache

	## IMPOSTAZIONI ------------------------------------------------------------
	
	def carica_codici_comuni(self, nome_file):
		# carico il file con i codici dei comuni/ecc. Il file si trova in questa stessa cartella
		path_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), nome_file)
	
		self.codici_comuni, self.codici_province, self.codici_regioni = codici_enti(path_file)
	
	def set_urls(self, id_url, item_urls):
		self.dict_url[id_url] = item_urls
		return self

	## UTILS -------------------------------------------------------------------
	
	def calcola_enti_pervenuti(self, nome_cartella):
		# prendo gli ultimi due enti_pervenuti e faccio la differenza
		list_files = [file_i for file_i 
			in os.listdir(os.path.join(self.base_folder, nome_cartella))
			if 'enti_pervenuti' in file_i and 'ULTIMO' not in file_i]
			
		if len(list_files) < 2:
			return []

		perv_ult, perv_penult = sorted(list_files, reverse=True)[0:2]
		
		with open(os.path.join(self.base_folder, nome_cartella, perv_ult), 'r') as f: 
			perv_ult = json.load(f)

		with open(os.path.join(self.base_folder, nome_cartella, perv_penult), 'r') as f: 
			perv_penult = json.load(f)
		
		# nomi dei comuni che sono nell'ultimo pervenuti ma non sono nel pervenuti precedente
		list_ultimi_comuni_pervenuti = [ente_i['cm'] for ente_i in perv_ult['enti'] if ente_i not in perv_penult['enti']]
		log(list_ultimi_comuni_pervenuti, style='note')

		# adesso devo trovare il codice comune per ogni comune
		list_ultimi_comuni_pervenuti = [self.codici_comuni[cod_i] for cod_i in list_ultimi_comuni_pervenuti]
		
		return list_ultimi_comuni_pervenuti
		
	def costruisci_item_url_scrutini(self, list_codici_ente):
		return [
			[
				calc_url_ente(codice_ente),
				'{}/scrutini/scrutini_{}-{}-.json'.format('{}', codice_ente, '{}'),
				[['Referer', 'https://elezioni.interno.gov.it/regionali/scrutini/20190324/scrutiniRI{}'.format(codice_ente)]]
			] 
			for codice_ente in list_codici_ente
		]
	
	## SCARICAMENTO ------------------------------------------------------------

	# lo scaricamento funziona nel seguente modo:
	# 1) dallo script principale viene chiamata la funzione scarica(id_url) con l'id
	#		con cui sono stati memorizzati gli url voluti
	#		( ad esempio se voglio scaricare gli ultimi enti pervenuti )
	# 2) scarica() chiama scarica_files che per ogni url costruisce il percorso
	#		gli header e poi scarica

	def scarica_files(self, list_urls):
		for url_i, filename_out_i, additional_headers_i in list_urls:
		
			path_out = filename_out_i.format(
				base_folder=self.base_folder, 
				timestamp=current_time()
			)
		
			# controllo nella cache se saltare o no l'url
			if self.cache != None:
				if self.cache.get_url(url_i) == False:
					log('SKIPPED {}'.format(url_i), style='log')
					return
		
			scarica_file(
				url_i, 
				headers=dict(self.base_headers + additional_headers_i), 
				path_out=path_out
			)
			
	def scarica(self, id_url):
		# scarico gli url che ho memorizzato con l'id id_url
		self.scarica_files(self.dict_url[id_url])
			

			
			
			
			
			
			
			
			
			

