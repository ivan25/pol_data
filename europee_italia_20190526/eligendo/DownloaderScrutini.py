from .Downloader import Downloader

class DownloaderScrutini(Downloader):

	# elemento di enti
	# [{'cod': '3080300290', 'desc': '<nome comune>', 'tipo': 'CM', 'tipo_comune': 'M', 'dt_agg': 20190508230703}]

	# https://eleapi.interno.gov.it/siel/PX/scrutiniEI/TE/01/RE/08						reg
	# https://elezioni.interno.gov.it/europee/scrutini/20190526/scrutiniEI3080000000
	
	# https://eleapi.interno.gov.it/siel/PX/scrutiniEI/TE/01/PR/042						prov
	# https://elezioni.interno.gov.it/europee/scrutini/20190526/scrutiniEI3080420000
	
	# https://eleapi.interno.gov.it/siel/PX/scrutiniEI/TE/01/PR/042/CM/0320				com
	# https://elezioni.interno.gov.it/europee/scrutini/20190526/scrutiniEI3080420320

	def calcola_urls_enti_superiori(self, list_codici_comuni):
		pad0 = lambda s, n: s + '0' * (n - len(s))
	
		list_urls = []
		
		for cod_com in list_codici_comuni:
			for ente_i in self.calc_enti_sup_da_comune(cod_com):
				url_i = [
					'https://eleapi.interno.gov.it/siel/PX/scrutiniEI/TE/01/{tree}'.format(**ente_i),
					"{base_folder}/scrutini/scrutini_{tree_noslash}_-{timestamp}-.json".format(**ente_i),
					[[
						"Referer", 
						"https://elezioni.interno.gov.it/europee/scrutini/20190526/scrutiniEI{}".format(
							pad0(ente_i['cod_com'], 10)
						)
					]]
				]
			
				if url_i not in list_urls:
					list_urls.append(url_i)
				
		return list_urls
		
	def calc_enti_sup_da_comune(self, cod_com):
		# dato il codice di un comune estraggo il codice della provincia e regione associata
		
		#	curl 'https://eleapi.interno.gov.it/siel/PX/votanti/TE/08/PR/042' 
		#	-H 'Referer: https://elezioni.interno.gov.it/comunali/votanti/20190526/votantiGI08042'
		
		# ritorno
		yield {'cod_com': cod_com[1:3], 'tree': 'RE/{}'.format(cod_com[1:3]), 
				'tree_noslash': 'RE_{}'.format(cod_com[1:3]),
				'timestamp': '{timestamp}', 'base_folder': '{base_folder}'}		
		yield {'cod_com': cod_com[0:6], 'tree': 'PR/{}'.format(cod_com[3:6]), 
				'tree_noslash': 'PR_{}'.format(cod_com[3:6]),
				'timestamp': '{timestamp}', 'base_folder': '{base_folder}'}
		yield {'cod_com': cod_com, 'tree': 'PR/{}/CM/{}'.format(cod_com[3:6], cod_com[6:10]), 
				'tree_noslash': 'PR_{}_CM_{}'.format(cod_com[3:6], cod_com[6:10]),
				'timestamp': '{timestamp}', 'base_folder': '{base_folder}'}
