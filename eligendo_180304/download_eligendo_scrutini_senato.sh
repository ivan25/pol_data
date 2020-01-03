mkdir -p ~/Scrivania/dati_eligendo/eligendo_senato
cd ~/Scrivania/dati_eligendo/eligendo_senato

while [ 1 ]
do
    hour=$(date '+%H')
	minute=$(date '+%M')
	second=$(date '+%S')
	
	curl 'http://elezioni.interno.gov.it/politiche/senato20180304/scrutiniSI' -H 'Cookie: _ga=GA1.3.306968677.1514503186' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: en-US,en;q=0.9,it;q=0.8' -H 'User-Agent: Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/64.0.3282.167 Chrome/64.0.3282.167 Safari/537.36' -H 'Content-Type: application/json' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Referer: http://elezioni.interno.gov.it/senato/scrutini/20180304/scrutiniSI' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' --compressed -o ./eligendo_risultati_senato_180306_$hour$minute$second.json
    
    curl 'http://elezioni.interno.gov.it/politiche/senato20180304/elenchiSI' -H 'Cookie: _ga=GA1.3.306968677.1514503186' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: en-US,en;q=0.9,it;q=0.8' -H 'User-Agent: Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/64.0.3282.167 Chrome/64.0.3282.167 Safari/537.36' -H 'Content-Type: application/json' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Referer: http://elezioni.interno.gov.it/senato/scrutini/20180304/elenchiSI' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' --compressed -o ./eligendo_elenchi_senato_180306_$hour$minute$second.json
    
    curl 'http://elezioni.interno.gov.it/politiche/camera20180304/ultimipervCI' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Referer: http://elezioni.interno.gov.it/camera/scrutini/20180304/ultimipervCI' -H 'X-Requested-With: XMLHttpRequest' -H 'User-Agent: Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/64.0.3282.167 Chrome/64.0.3282.167 Safari/537.36' --compressed -o ./eligendo_ultimienti_180306_$hour$minute$second.json
    
    curl 'http://elezioni.interno.gov.it/politiche/camera20180304/scrutiniCI' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Referer: http://elezioni.interno.gov.it/camera/scrutini/20180304/scrutiniCI' -H 'X-Requested-With: XMLHttpRequest' -H 'User-Agent: Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/64.0.3282.167 Chrome/64.0.3282.167 Safari/537.36' --compressed -o ./eligendo_risultati_camera_180306_$hour$minute$second.json
    
    curl 'http://elezioni.interno.gov.it/politiche/camera20180304/elenchiCI' -H 'Cookie: _ga=GA1.3.306968677.1514503186' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: en-US,en;q=0.9,it;q=0.8' -H 'User-Agent: Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/64.0.3282.167 Chrome/64.0.3282.167 Safari/537.36' -H 'Content-Type: application/json' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Referer: http://elezioni.interno.gov.it/camera/scrutini/20180304/elenchiCI' -H 'X-Requested-With: XMLHttpRequest' --compressed -o ./eligendo_elenchi_camera_180306_$hour$minute$second.json
    
    sleep 180
done
