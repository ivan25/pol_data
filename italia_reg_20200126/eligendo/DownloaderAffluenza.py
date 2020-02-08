from .Downloader import Downloader
from .utils import log

"""
	Come funziona lo scarico dei dati dell'affluenza
	1) si imposta la classe (con i percorsi, gli header base ecc)
	
	2) periodicamente (while True: time.sleep()) scarico gli enti pervenuti
	3) calcolo quali sono gli enti pervenuti (facendo la differenza tra gli ultimi due file)
	4) calcolo regione e provincia dei comuni pervenuti , perche' per l'affluenza non devo
		scaricare le pagine dei singoli comuni, ma mi basta la pagina della provincia,
		dove cosi' prendo anche tutti gli altri comuni a gratis e faccio meno richieste
		
		https://eleapi.interno.gov.it/siel/PX/votanti/TE/01										italia
		https://eleapi.interno.gov.it/siel/PX/votanti/TE/01/RE/08				3080000000		regione aa
		https://eleapi.interno.gov.it/siel/PX/votanti/TE/01/PR/042				3080420000		prov bb
		https://eleapi.interno.gov.it/siel/PX/scrutiniG/TE/08/PR/042/CM/0320	3080420320		comune cc
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

	def estrai_cod_da_entiperv(self, ente_i):
		# ente_i['cm'] e' il nome testuale del comune, quindi per estrarre il codice
		# del comune bisogna andare dentro self.codici_comuni
		# cod_cm e' della forma 080130130080
		#                       ^^           regione
		#                         ^^^        circoscrizione
		#                            ^^^     provincia
		#                               ^^^^ comune
		
		try:
			cod_cm = self.codici_comuni[ente_i['cm']]
		
			return (
				cod_cm[8:12],
				cod_cm[5:8], 
				cod_cm[2:5], 
				cod_cm[0:2]
			)
		except:
			log('error DownloaderAffluenza estrai_cod_da_entiperv ' + ente_i['cm'], style='error')
			return None

	def calcola_urls_enti_superiori(self, list_codici_comuni):

		list_urls = []
		
		for (cod_com, cod_pro, cod_circ, cod_reg) in list_codici_comuni:
		
			for ente_i in self.calc_enti_sup_da_comune(cod_com, cod_pro, cod_circ, cod_reg):
			
				url_i = [
					'https://eleapi.interno.gov.it/siel/PX/votanti/TE/07/{tree}'.format(**ente_i),
					"{base_folder}/votanti/votanti_{tree_noslash}_-{timestamp}-.json".format(**ente_i),
					[[
						"Referer", 
						"https://elezioni.interno.gov.it/regionali/votanti/20200126/votantiRI{referer}".format(**ente_i)
					]]
				]
			
				if url_i not in list_urls:
					list_urls.append(url_i)
				
		return list_urls
		
	def calc_enti_sup_da_comune(self, cod_com, cod_pro, cod_circ, cod_reg):
		# dato il codice di un comune estraggo il gli elementi per costruire la richiesta per il comune
		# stesso e la provincia di cui fa parte (eventualmente se voglio anche della regione)
		
		# ritorno gli enti superiori a partire dal comune dato
		
		# regione
		yield {
			'tree': 'RE/{reg:0>2}'.format(reg = cod_reg), 
			'tree_noslash': 'RE_{reg:0>2}'.format(reg = cod_reg), 
			'referer': '{reg:0>2}{pro:0>3}'.format(reg = cod_reg, pro = 0),
			'timestamp': '{timestamp}', 
			'base_folder': '{base_folder}'
		}
		
		# provincia
		yield {
			'tree': 'PR/{pro:0>3}'.format(
				reg = cod_reg, pro = cod_pro
			), 
			'tree_noslash': 'PR_{pro:0>3}'.format(
				reg = cod_reg, pro = cod_pro
			),
			'referer': '{reg:0>2}{pro:0>3}'.format(
				reg = cod_reg, pro = cod_pro
			),
			'timestamp': '{timestamp}', 
			'base_folder': '{base_folder}'
		}
