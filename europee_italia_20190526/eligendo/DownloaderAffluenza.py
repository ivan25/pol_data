from .Downloader import Downloader

"""
	Come funziona lo scarico dei dati dell'affluenza
	1) si imposta la classe (con i percorsi, gli header base ecc)
	
	2) periodicamente (while True: time.sleep()) scarico gli enti pervenuti
	3) calcolo quali sono gli enti pervenuti (facendo la differenza tra gli ultimi due file)
	4) calcolo regione e provincia dei comuni pervenuti , perche' per l'affluenza non devo
		scaricare le pagine dei singoli comuni, ma mi basta la pagina della provincia,
		dove cosi' prendo anche tutti gli altri comuni a gratis e faccio meno richieste
		
		https://eleapi.interno.gov.it/siel/PX/votanti/TE/01										italia
		https://eleapi.interno.gov.it/siel/PX/votanti/TE/01/RE/08				3080000000		regione
		https://eleapi.interno.gov.it/siel/PX/votanti/TE/01/PR/042				3080420000		prov
		https://eleapi.interno.gov.it/siel/PX/scrutiniG/TE/08/PR/042/CM/0220	3080420220		comune
																				xxx				regione
																				   xxx			provincia
																				      xxxx		comune
	5) scarico i file e li salvo

"""

class DownloaderAffluenza(Downloader):
	
	# https://eleapi.interno.gov.it/siel/PX/votanti/TE/01/RE/08
	# https://elezioni.interno.gov.it/europee/votanti/20190526/votantiEI08000

	# https://eleapi.interno.gov.it/siel/PX/votanti/TE/01/PR/042
	# https://elezioni.interno.gov.it/europee/votanti/20190526/votantiEI08042

	def calcola_urls_enti_superiori(self, list_codici_comuni):
		pad0 = lambda s, n: s + '0' * (n - len(s))
	
		list_urls = []
		template_url = [
			"https://eleapi.interno.gov.it/siel/PX/votanti/TE/01/{tipo_ente}/{cod_ente}", 
			"{base_folder}/votanti/votanti_{tipo_ente}_{cod_ente}_-{timestamp}-.json",
			[["Referer", "https://elezioni.interno.gov.it/europee/votanti/20190526/votantiEI{}"]]
		]
		
		for cod_com in list_codici_comuni:
			for ente_i in self.calc_enti_sup_da_comune(cod_com):
				url_i = [
					template_url[0].format(**ente_i),
					template_url[1].format(**ente_i),
					[[
						"Referer", 
						"https://elezioni.interno.gov.it/europee/votanti/20190526/votantiEI{}".format(
							pad0(ente_i['cod_ente'], 5)
						)
					]]
				]
			
				if url_i not in list_urls:
					list_urls.append(url_i)
				
		return list_urls
		
	def calc_enti_sup_da_comune(self, cod_com):
		# dato il codice di un comune estraggo il codice della provincia e regione associata
		
		#	curl 'https://eleapi.interno.gov.it/siel/PX/votanti/TE/08/PR/052' 
		#	-H 'Referer: https://elezioni.interno.gov.it/comunali/votanti/20190526/votantiGI08052'
		
		# ritorno
		#yield {'tipo_ente': 'RE', 'cod_ente': cod_com[0:3], 'timestamp': '{timestamp}', 'base_folder': '{base_folder}'}
		yield {'tipo_ente': 'PR', 'cod_ente': cod_com[3:6], 'timestamp': '{timestamp}', 'base_folder': '{base_folder}'}
		
	
	
	
	
	
	
	
	
	
	
	
	
	
	
