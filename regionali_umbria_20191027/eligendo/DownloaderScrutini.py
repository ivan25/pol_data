from .Downloader import Downloader

class DownloaderScrutini(Downloader):

	# elemento di enti
	# [{'cod': '3080300190', 'desc': '<COMUNE>', 'tipo': 'CM', 'tipo_comune': 'M', 'dt_agg': 20190508230703}]

	# https://eleapi.interno.gov.it/siel/PX/scrutiniEI/TE/01/RE/08						reg aa
	# https://elezioni.interno.gov.it/europee/scrutini/20190526/scrutiniEI3080000000
	
	# https://eleapi.interno.gov.it/siel/PX/scrutiniEI/TE/01/PR/042						prov bb
	# https://elezioni.interno.gov.it/europee/scrutini/20190526/scrutiniEI3080420000
	
	# https://eleapi.interno.gov.it/siel/PX/scrutiniEI/TE/01/PR/042/CM/0320				com cc
	# https://elezioni.interno.gov.it/europee/scrutini/20190526/scrutiniEI3080420320

	def calcola_urls_enti_superiori(self, list_codici_comuni):
		pad0 = lambda s, n: str(s) + '0' * (n - len(str(s)))
	
		list_urls = []
		
		for (cod_com, cod_pro) in list_codici_comuni:
			for ente_i in self.calc_enti_sup_da_comune(cod_com, cod_pro):
				url_i = [
					'https://eleapi.interno.gov.it/siel/PX/scrutiniR/TE/07/{tree}'.format(**ente_i),
					"{base_folder}/scrutini/scrutini_{tree_noslash}_-{timestamp}-.json".format(**ente_i),
					[[
						"Referer", 
						"https://elezioni.interno.gov.it/regionali/scrutini/20191027/scrutiniRI{}".format(
							pad0(ente_i['cod_com'], 10)
						)
					]]
				]
			
				if url_i not in list_urls:
					list_urls.append(url_i)
				
		return list_urls
		
	def calc_enti_sup_da_comune(self, cod_com, cod_pro):
		# dato il codice di un comune estraggo il codice della provincia e regione associata
		
		pad0 = lambda s, n: '0' * (n - len(str(s))) + str(s)
		
		#	curl 'https://eleapi.interno.gov.it/siel/PX/votanti/TE/08/PR/062' 
		#	-H 'Referer: https://elezioni.interno.gov.it/comunali/votanti/20190526/votantiGI09062'
		
		# ritorno
		#yield {'cod_com': cod_com[1:3], 'tree': 'RE/10', 
		#		'tree_noslash': 'RE_10',
		#		'timestamp': '{timestamp}', 'base_folder': '{base_folder}'}		
		#yield {'tree': 'RE/10/PR/{}'.format(pad0(cod_pro, 3)), 
		#		'tree_noslash': 'RE_10_PR_{}'.format(pad0(cod_pro, 3)),
		#		'timestamp': '{timestamp}', 'base_folder': '{base_folder}'}
				
		yield {'cod_com': cod_com, 'tree': 'RE/10/PR/{}/CM/{}'.format(pad0(cod_pro, 3), pad0(cod_com, 4)), 
				'tree_noslash': 'RE_10_PR_{}_CM_{}'.format(pad0(cod_pro, 3), pad0(cod_com, 4)),
				'timestamp': '{timestamp}', 'base_folder': '{base_folder}'}
