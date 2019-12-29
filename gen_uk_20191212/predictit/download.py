import time, json
import requests
from datetime import datetime

def download(url, path_out):
	data = requests.get(url).json()

	with open(path_out, 'w') as f:
		json.dump(data, f, indent=2, sort_keys=True)

	return data

def print_pm(data):
	d_bojo = [d for d in data if d['contractName'] == 'Boris Johnson'][0]
	d_jc = [d for d in data if d['contractName'] == 'Jeremy Corbyn'][0]

	p_bojo = d_bojo['lastTradePrice']
	p_jc = d_jc['lastTradePrice']

	#print('\t\t\t\t\t{}\t{}'.format(d_bojo['lastTradePrice'], d_jc['lastTradePrice']))
	print(
		' '*int(min(p_bojo, p_jc)*200) + '{}'.format(int(min(p_bojo, p_jc)*100)) + 
			' '*int((max(p_bojo, p_jc)-min(p_bojo, p_jc))*200) + '{}'.format(int(max(p_bojo, p_jc)*100))
	)

while True:
	timestamp = datetime.now().strftime('-%Y_%m_%d-%H_%M_%S-')
	
	if i % 10 == 0:
		print(timestamp)

	data = download('https://www.predictit.org/api/Market/6077/Contracts',
				'<>/predictit_20191212/data/pmcontracts_{}.json'.format(timestamp))

	download('https://www.predictit.org/api/Market/6163/Contracts',
				'<>/predictit_20191212/data/conseatscontracts_{}.json'.format(timestamp))

	download('https://www.predictit.org/api/Market/6164/Contracts',
				'<>/predictit_20191212/data/labseatscontracts_{}.json'.format(timestamp))

	time.sleep(30)
