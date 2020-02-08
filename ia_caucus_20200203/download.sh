#!/bin/bash

cd ./ia_caucus_20200203/

uagent=""

while true; do
	echo $(date +'-%Y_%m_%d-%H_%M_%S-%Z-')

	curl 'https://www.predictit.org/api/Market/3633/Contracts' -H "$uagent" -H 'Accept: application/json, text/plain, */*' -H 'Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3' --compressed -H 'Referer: https://www.predictit.org/markets/detail/3633/Who-will-win-the-2020-Democratic-presidential-nomination' -H 'DNT: 1' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' | \
		jq '.' \
		> "./data/predictit_contracts_$(TZ=':US/Central' date +'-%Y_%m_%d-%H_%M_%S-%Z-').json"

	curl 'https://www.predictit.org/api/Market/3698/Contracts' -H "$uagent" -H 'Accept: application/json, text/plain, */*' -H 'Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3' --compressed -H 'Referer: https://www.predictit.org/markets/detail/3698/Who-will-win-the-2020-US-presidential-election' -H 'DNT: 1' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' | \
		jq '.' \
		> "./data/predictit_contracts-2020_$(TZ=':US/Central' date +'-%Y_%m_%d-%H_%M_%S-%Z-').json"

	curl 'https://www.predictit.org/api/Market/5241/Contracts' -H "$uagent" -H 'Accept: application/json, text/plain, */*' -H 'Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3' --compressed -H 'Referer: https://www.predictit.org/markets/detail/5241/Who-will-win-the-2020-Iowa-Democratic-caucuses' -H 'DNT: 1' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' | \
		jq '.' \
		> "./data/predictit_contracts-iowa_$(TZ=':US/Central' date +'-%Y_%m_%d-%H_%M_%S-%Z-').json"

	curl 'https://www.politico.com/2020-election/data/live-results/2020-02-03/iowa/county.csv' -H "$uagent" \
		> "./data/politico_county_$(TZ=':US/Central' date +'-%Y_%m_%d-%H_%M_%S-%Z-').csv"
	
	curl 'https://feeds-elections.foxnews.com/archive/politics/elections/2020/1/2020_primary_caucus/R_primary/IA/state_level_results/file.json' -H "$uagent" | \
		jq '.' \
		> "./data/foxnews_stateR_$(TZ=':US/Central' date +'-%Y_%m_%d-%H_%M_%S-%Z-').json"
	
	curl 'https://feeds-elections.foxnews.com/archive/politics/elections/2020/1/2020_primary_caucus/D_primary/IA/county_level_results/file.json' -H "$uagent" | \
		jq '.' \
		> "./data/foxnews_countyD_$(TZ=':US/Central' date +'-%Y_%m_%d-%H_%M_%S-%Z-').json"
	
	curl 'https://feeds-elections.foxnews.com/archive/politics/elections/2020/1/2020_primary_caucus/R_primary/IA/county_level_results/file.json' -H "$uagent" | \
		jq '.' \
		> "./data/foxnews_countyR_$(TZ=':US/Central' date +'-%Y_%m_%d-%H_%M_%S-%Z-').json"
	
	curl 'https://feeds-elections.foxnews.com/archive/politics/elections/2020/1/2020_primary_caucus/D_primary/IA/state_level_results/file.json' -H "$uagent" | \
		jq '.' \
		> "./data/foxnews_stateD_$(TZ=':US/Central' date +'-%Y_%m_%d-%H_%M_%S-%Z-').json"	
	
	curl 'https://int.nyt.com/applications/elections/2020/data/api/2020-02-03/iowa/president/democrat.json' -H "$uagent" -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3' --compressed -H 'Referer: https://www.nytimes.com/' -H 'Origin: https://www.nytimes.com' -H 'DNT: 1' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'TE: Trailers' | \
		jq '.' \
		> "./data/nyt_county_$(TZ=':US/Central' date +'-%Y_%m_%d-%H_%M_%S-%Z-').json"
	
	curl 'https://int.nyt.com/applications/elections/2020/data/liveModel/2020-02-03/ia-17275-2020-02-03.json' -H "$uagent" -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3' --compressed -H 'Referer: https://www.nytimes.com/' -H 'Origin: https://www.nytimes.com' -H 'DNT: 1' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'TE: Trailers' | \
		jq '.' \
		> "./data/nyt_estimate_$(TZ=':US/Central' date +'-%Y_%m_%d-%H_%M_%S-%Z-').json"
	
	curl 'https://results.thecaucuses.org/' -H "$uagent" -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' -H 'Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3' --compressed -H 'DNT: 1' -H 'Connection: keep-alive' -H 'Upgrade-Insecure-Requests: 1' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'TE: Trailers' \
		> "./data/thecaucuses_$(TZ=':US/Central' date +'-%Y_%m_%d-%H_%M_%S-%Z-').html"
	
	precintreporting=$(cat $(ls ./data/politico_county_*.csv | tail -n 1) | awk -F "," '(NR==2) { print $7 }')
	echo $precintreporting
	
	sleep $(( 5*60 ))
	
done
