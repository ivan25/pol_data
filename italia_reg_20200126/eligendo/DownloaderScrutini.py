from .Downloader import Downloader

class DownloaderScrutini(Downloader):

	# elemento di enti
	# [{'cod': '3080300190', 'desc': '<COMUNE>', 'tipo': 'CM', 'tipo_comune': 'M', 'dt_agg': 20190508230703}]

	# https://eleapi.interno.gov.it/siel/PX/scrutiniR/TE/07/RE/08/CR/101					prov 
	# https://elezioni.interno.gov.it/regionali/scrutini/20200126/scrutiniRI081011010000

	# https://eleapi.interno.gov.it/siel/PX/scrutiniR/TE/07/RE/08/PR/101/CM/0130			com 
	# https://elezioni.interno.gov.it/regionali/scrutini/20200126/scrutiniRI081011010130

	def estrai_cod_da_entiperv(self, ente_i):
		# Negli enti pervenuti dello scrutinio sono presenti direttamente i codici nel json
		return (
			ente_i['cod_com'], 
			ente_i['cod_prov'], 
			ente_i['cod_circ'], 
			ente_i['cod_reg']
		)

	def calcola_urls_enti_superiori(self, list_codici_comuni):

		list_urls = []
		
		for (cod_com, cod_pro, cod_circ, cod_reg) in list_codici_comuni:
		
			for ente_i in self.calc_enti_sup_da_comune(cod_com, cod_pro, cod_circ, cod_reg):
			
				url_i = [
					'https://eleapi.interno.gov.it/siel/PX/scrutiniR/TE/07/{tree}'.format(**ente_i),
					"{base_folder}/scrutini/scrutini_{tree_noslash}_-{timestamp}-.json".format(**ente_i),
					[[
						"Referer", 
						"https://elezioni.interno.gov.it/regionali/scrutini/20200126/scrutiniRI{referer}".format(**ente_i)
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
			'referer': '{reg:0>2}{circ:0>3}{pro:0>3}{com:0>4}'.format(
				reg = cod_reg, circ = 0, pro = 0, com = 0
			),
			'timestamp': '{timestamp}', 
			'base_folder': '{base_folder}'		
		}
		
		# provincia/circoscrizione
		if cod_circ == cod_pro:
			# i codici della circoscrizione e della provincia sono uguali, quindi
			# la provincia coincide con la circoscrizione, quindi per ottenere l'url
			# degli scrutini nella provincia devo mettere il codice della circoscrizione
			yield {
				'tree': 'RE/{reg:0>2}/CR/{circ:0>3}'.format(
					reg = cod_reg, circ = cod_circ
				), 
				'tree_noslash': 'RE_{reg:0>2}_CR_{circ:0>3}'.format(
					reg = cod_reg, circ = cod_circ
				),
				'referer': '{reg:0>2}{circ:0>3}{pro:0>3}{com:0>4}'.format(
					reg = cod_reg, circ = cod_circ, pro = cod_pro, com = 0
				),
				'timestamp': '{timestamp}', 
				'base_folder': '{base_folder}'
			}
		else:
			# altrimenti se sono diversi metto quello della provincia
			yield {
				'tree': 'RE/{reg:0>2}/PR/{pro:0>3}'.format(
					reg = cod_reg, pro = cod_pro
				), 
				'tree_noslash': 'RE_{reg:0>2}_PR_{pro:0>3}'.format(
					reg = cod_reg, pro = cod_pro
				),
				'referer': '{reg:0>2}{circ:0>3}{pro:0>3}{com:0>4}'.format(
					reg = cod_reg, circ = cod_circ, pro = cod_pro, com = 0
				),
				'timestamp': '{timestamp}', 
				'base_folder': '{base_folder}'
			}			
				
		# comune
		yield {
			'tree': 'RE/{reg:0>2}/PR/{pro:0>3}/CM/{com:0>4}'.format(
				reg = cod_reg, pro = cod_pro, com = cod_com
			), 
			'tree_noslash': 'RE_{reg:0>2}_PR_{pro:0>3}_CM_{com:0>4}'.format(
				reg = cod_reg, pro = cod_pro, com = cod_com
			),
			'referer': '{reg:0>2}{circ:0>3}{pro:0>3}{com:0>4}'.format(
				reg = cod_reg, circ = cod_circ, pro = cod_pro, com = cod_com
			),
			'timestamp': '{timestamp}', 
			'base_folder': '{base_folder}'
		}
