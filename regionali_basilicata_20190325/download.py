import requests as req
import json, os
from datetime import datetime

base_folder = '~/Scrivania/eligendo_basilicata'

# header che sono comuni a tutte le richieste
common_headers = [
	['Host', 'eleapi.interno.gov.it'],
	['User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0'],
	['Accept', 'application/json, text/javascript, */*; q=0.01'],
	['Accept-Language', 'it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3'],
	['DNT', '1'],
	['Connection', 'keep-alive'],
	['Content-Type', 'application/json'],
	['Origin', 'https://elezioni.interno.gov.it'],
	['Accept-Encoding', 'gzip, deflate, br']
]

# gli url sono: url della richiesta get, nome del file da salvare, header specifici in piu' a quelli comuni a tutti
list_urls_pervenuti_votanti = [
	[
		'https://eleapi.interno.gov.it/siel/PX/votaultimi/TE/07', '{}/votanti/votanti_enti_pervenuti-{}-.json',
		[['Referer', 'https://elezioni.interno.gov.it/regionali/votanti/20190324/votantiultimiRI']]
	]
]

list_urls_votanti = [
	[
		'https://eleapi.interno.gov.it/siel/PX/votanti/TE/07/RE/17', '{}/votanti/votanti_basilicata-{}-.json',
		[['Referer', 'https://elezioni.interno.gov.it/regionali/votanti/20190324/votantiRI17047']]
	],
	[
		'https://eleapi.interno.gov.it/siel/PX/votanti/TE/07/PR/047', '{}/votanti/votanti_matera-{}-.json', 
		[['Referer', 'https://elezioni.interno.gov.it/regionali/votanti/20190324/votantiRI17047']]
	],
	[
		'https://eleapi.interno.gov.it/siel/PX/votanti/TE/07/PR/064', '{}/votanti/votanti_potenza-{}-.json', 
		[['Referer', 'https://elezioni.interno.gov.it/regionali/votanti/20190324/votantiRI17047']]
	]
]

list_urls_scrutini_pervenuti = [
	[
		'https://eleapi.interno.gov.it/siel/PX/scruultimiR/TE/07', '{}/scrutini/scrutini_enti_pervenuti-{}-.json',
		[['Referer', 'https://elezioni.interno.gov.it/regionali/scrutini/20190324/ultimipervRI']]
	]
]

list_urls_scrutini = [
	[
		'https://eleapi.interno.gov.it/siel/PX/scrutiniR/TE/07/RE/17', '{}/scrutini/scrutini_basilicata-{}-.json',
		[['Referer', 'https://elezioni.interno.gov.it/regionali/scrutini/20190324/scrutiniRI170000000000']]
	],
	[
		'https://eleapi.interno.gov.it/siel/PX/scrutiniR/TE/07/RE/17/CR/047', '{}/scrutini/scrutini_matera-{}-.json',
		[['Referer', 'https://elezioni.interno.gov.it/regionali/scrutini/20190324/scrutiniRI170470470000']]
	],
	[
		'https://eleapi.interno.gov.it/siel/PX/scrutiniR/TE/07/RE/17/CR/064', '{}/scrutini/scrutini_potenza-{}-.json',
		[['Referer', 'https://elezioni.interno.gov.it/regionali/scrutini/20190324/scrutiniRI170640640000']]
	],
	[
		'https://eleapi.interno.gov.it/siel/PX/elenchiR/TE/07/RE/17', '{}/scrutini/scrutini_elenchi_basilicata-{}-.json',
		[['Referer', 'https://elezioni.interno.gov.it/regionali/scrutini/20190324/elenchiRI17000000']]
	],
	[
		'https://eleapi.interno.gov.it/siel/PX/elenchiR/TE/07/RE/17/CR/047', '{}/scrutini/scrutini_elenchi_matera-{}-.json',
		[['Referer', 'https://elezioni.interno.gov.it/regionali/scrutini/20190324/elenchiRI17047047']]
	],
	[
		'https://eleapi.interno.gov.it/siel/PX/elenchiR/TE/07/RE/17/CR/064', '{}/scrutini/scrutini_elenchi_potenza-{}-.json',
		[['Referer', 'https://elezioni.interno.gov.it/regionali/scrutini/20190324/elenchiRI17064064']]
	]
]

# ------------------------------------------------------------------------------

def scarica_file(list_urls):
	for url_i, filename_out_i, additional_headers_i in list_urls:
		try:
			response = req.get(url_i, headers=dict(common_headers+additional_headers_i))

			# genero il path dove salvare il file
			path_out_i = filename_out_i.format(base_folder, current_time)
			path_out_last_i = filename_out_i.format(base_folder, 'ULTIMO')
			
			print '{} -> {}'.format(url_i, path_out_i)

			with open(path_out_i, 'w') as f:
				json.dump(response.json(), f, indent=2)
				
		#	with open(path_out_last_i, 'w') as f:
		#		json.dump(response.json(), f, indent=2)
		except Exception, e:
			print e

def calcola_enti_pervenuti(nome_cartella):
	# prendo gli ultimi due enti_pervenuti e faccio la differenza
	perv_ult, perv_penult = sorted(
		[d for d in os.listdir('{}/{}'.format(base_folder, nome_cartella)) if 'enti_pervenuti' in d and 'ULTIMO' not in d],
		reverse = True
	)[0:2]
	
	with open('{}/{}/{}'.format(base_folder, nome_cartella, perv_ult), 'r') as f: perv_ult = json.load(f)
	with open('{}/{}/{}'.format(base_folder, nome_cartella, perv_penult), 'r') as f: perv_penult = json.load(f)
	
	# nomi dei comuni che sono nell'ultimo pervenuti ma non sono nel pervenuti precedente
	list_ultimi_comuni_pervenuti = [ente_i['cm'] for ente_i in perv_ult['enti'] if ente_i not in perv_penult['enti']]
	print list_ultimi_comuni_pervenuti
	# adesso devo trovare il codice comune per ogni comune
	list_ultimi_comuni_pervenuti = [dict_codici[cod_i] for cod_i in list_ultimi_comuni_pervenuti]
	
	return list_ultimi_comuni_pervenuti

# ------------------------------------------------------------------------------

with open('~/Scrivania/eligendo_basilicata/regionali_territoriale_italia.json', 'r') as f:
	dict_codici = json.load(f)
	dict_codici = [ente_i for ente_i in dict_codici['enti'] if ente_i['tipo'] == 'CM']
	dict_codici = {ente_i['desc']: ente_i['cod'] for ente_i in dict_codici}

# codice comune e' del tipo e lo converto in url del tipo 
# 012345678901
# 170470470010		https://eleapi.interno.gov.it/siel/PX/scrutiniR/TE/07/RE/17/PR/047/CM/0010
# 170640640020		https://eleapi.interno.gov.it/siel/PX/scrutiniR/TE/07/RE/17/PR/064/CM/0020
# referer invece e'	https://elezioni.interno.gov.it/regionali/scrutini/20190324/scrutiniRI170470470010
calc_url_comune = lambda codice_comune: 'https://eleapi.interno.gov.it/siel/PX/scrutiniR/TE/07/RE/17/PR/{}/CM/{}'.format(
	codice_comune[6:8], codice_comune[8:12]
)

print '\n\n-------------------------------------------'

# setto il timestamp inizialmente, in modo che se scarico molti file hanno tutti lo stesso timestamp
# e non invece tanti diversi separati da 1 secondo
current_time = datetime.now().strftime('%Y_%m_%d-%H_%M_%S')

# gli if True/False servono per selezionare quali parti eseguire (ad es inizialmente gli scrutini non
# ci sono ancora e si scaricano solo i votanti, dopo il contrario)

# scarico i dati dei votanti
if False:
	# scarico la lista degli enti pervenuti
	scarica_file(list_urls_pervenuti_votanti)
	
	list_ultimi_comuni_pervenuti = calcola_enti_pervenuti('votanti')

	# per gli scrutini siccome ho poche pagine da scaricare (in una pagina singola ci sono i dati di tutti
	# i comuni e quindi non devo scaricare una pagina per comune), volendo potrei scaricare tutte le pagine
	# ogni 15 secondo, ma si potrebbe fare di meglio: cioe' scaricare i dati solo quando ho nuovi enti pervenuti
	# (quindi testo se len(list_ultimi_comuni_pervenuti) > 0) in modo che io posso fare un loop anche ogni 5 sec
	# ma scarico solo quando arrivano dati e non scarico inutilmente (e quindi posso scaricare piu' fittamente)
	if len(list_ultimi_comuni_pervenuti) > 0:
		scarica_file(list_urls_votanti)

# prendo i nomi degli ultimi enti arrivati e scarico gli scrutini solo di quei comuni
# in modo da non scaricare continuamente centinaia di comuni con nessuna modifica
if False:
	# scarico i dati degli enti pervenuti scrutini
	scarica_file(list_urls_scrutini_pervenuti)
	
	# i dti degli scrutini li scarico solo una volta al minuto, non c'e bisogno di scaricarli
	# di continuo, visto che gia' scarico i dati dei singoli comuni
	if int(datetime.now().strftime('%S')) < 5:
		scarica_file(list_urls_scrutini)

	# calcolo quali sono gli enti pervenuti che non ho ancora visto, almeno scarico solo quelli
	list_ultimi_comuni_pervenuti = calcola_enti_pervenuti('scrutini')
	
	list_urls_comuni = [
		[
			calc_url_comune(codice_comune),
			'{}/scrutini_comuni/scrutini_comune_{}-{}-.json'.format('{}', codice_comune, '{}'),
			[['Referer', 'https://elezioni.interno.gov.it/regionali/scrutini/20190324/scrutiniRI{}'.format(codice_comune)]]
		] 
		for codice_comune in list_ultimi_comuni_pervenuti
	]
	
	scarica_file(list_urls_comuni)
	
# alla fine volendo posso scaricare i dati di tutti i comuni, per assicurarmi di non aver perso niente
if True:
	list_urls_comuni = [
		[
			calc_url_comune(codice_comune),
			'{}/scrutini_comuni/scrutini_comune_{}-{}-.json'.format('{}', codice_comune, '{}'),
			[['Referer', 'https://elezioni.interno.gov.it/regionali/scrutini/20190324/scrutiniRI{}'.format(codice_comune)]]
		] 
		for codice_comune in dict_codici.values()
	]
	
	scarica_file(list_urls_comuni)
