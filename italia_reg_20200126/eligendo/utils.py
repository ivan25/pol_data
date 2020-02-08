import json, os
from datetime import datetime
import requests as req
from sty import fg, bg, ef, rs, RgbFg

## LOG -------------------------------------------------------------------------

def log(message, style='log'):
	dict_styles = {
		'log': lambda s: print(str(s)),
		'note': lambda s: print(fg.cyan + str(s) + rs.fg),
		'headline': lambda s: print(fg.blue + bg.yellow + ef.bold + str(s) + rs.bold_dim + rs.bg + rs.fg),
		'error': lambda s: print(fg.white + bg.red + ef.bold + str(s) + rs.bold_dim + rs.bg + rs.fg)
	}
	
	dict_styles[style](message)
	
## DOWNLOAD --------------------------------------------------------------------
	
def scarica_file(url, headers, path_out):
	try:
		# tutti gli scaricamenti effettuati passano da qui
		response = req.get(url, headers=headers)

		with open(path_out, 'w') as f:
			json.dump(response.json(), f, indent=2, sort_keys=True)
		
		#with open(path_out, 'w') as f:
		#	f.write(response.text)
			
		log('{} -> {}'.format(url, path_out))
			
	#	with open(path_out_last_i, 'w') as f:
	#		json.dump(response.json(), f, indent=2)
	except Exception as e:
		log(f'err scarica_file {e}', style='error')
		
## ALTRO -----------------------------------------------------------------------
		
def current_time():
	return datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
	#return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	
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
