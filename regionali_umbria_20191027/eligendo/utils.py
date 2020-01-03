import json, os
from datetime import datetime
import requests as req
from sty import fg, bg, ef, rs, RgbFg

## LOG -------------------------------------------------------------------------

def log(message, style='log'):
	dict_styles = {
		'log': lambda s: print(str(s)),
		'note': lambda s: print(fg.cyan + str(s) + rs.fg),
		'headline': lambda s: print(fg.blue + bg.yellow + ef.bold + str(s) + rs.bold_dim + rs.bg + rs.fg)
	}
	
	dict_styles[style](message)
	
## DOWNLOAD --------------------------------------------------------------------
	
def scarica_file(url, headers, path_out):
	try:
		response = req.get(url, headers=headers)

		with open(path_out, 'w') as f:
			json.dump(response.json(), f, indent=2, sort_keys=True)
		
		#with open(path_out, 'w') as f:
		#	f.write(response.text)
			
		log('{} -> {}'.format(url, path_out))
			
	#	with open(path_out_last_i, 'w') as f:
	#		json.dump(response.json(), f, indent=2)
	except Exception as e:
		print(f'err scarica_file {e}')
		
## ALTRO -----------------------------------------------------------------------
		
def current_time():
	return datetime.now().strftime('%Y_%m_%d-%H_%M_%S')
	
def codici_enti(path_file):
	with open(path_file, 'r', encoding='latin1') as f:
		dict_codici = json.load(f)
		
	dict_codici_comuni = [ente_i for ente_i in dict_codici['enti'] if ente_i['tipo'] == 'CM']
	dict_codici_comuni = {ente_i['desc']: ente_i['cod'] for ente_i in dict_codici_comuni}
	
	dict_codici_province = [ente_i for ente_i in dict_codici['enti'] if ente_i['tipo'] == 'PR']
	dict_codici_province = {ente_i['desc']: ente_i['cod'] for ente_i in dict_codici_province}	
	
	dict_codici_regioni = [ente_i for ente_i in dict_codici['enti'] if ente_i['tipo'] == 'RE']
	dict_codici_regioni = {ente_i['desc']: ente_i['cod'] for ente_i in dict_codici_regioni}		
	
	return dict_codici_comuni, dict_codici_province, dict_codici_regioni

def calc_url_ente(codice_ente):
	# codice comune e' del tipo e lo converto in url del tipo 
	# 012345678901
	# 170470470010		https://eleapi.interno.gov.it/siel/PX/scrutiniR/TE/07/RE/17/PR/047/CM/0010
	# 170640640020		https://eleapi.interno.gov.it/siel/PX/scrutiniR/TE/07/RE/17/PR/064/CM/0020
	# referer invece e'	https://elezioni.interno.gov.it/regionali/scrutini/20190324/scrutiniRI170470470010
	return 'https://eleapi.interno.gov.it/siel/PX/scrutiniR/TE/07/RE/17/PR/{}/CM/{}'.format(
		codice_comune[6:8], codice_comune[8:12]
	)

def costruisci_item_url_scrutini(list_codici_ente):
	return [
		[
			calc_url_ente(codice_ente),
			'{}/scrutini/scrutini_{}-{}-.json'.format('{}', codice_ente, '{}'),
			[['Referer', 'https://elezioni.interno.gov.it/regionali/scrutini/20190324/scrutiniRI{}'.format(codice_ente)]]
		] 
		for codice_ente in list_codici_ente
	]
