const puppeteer = require('puppeteer');
const chalk = require('chalk');
const fs = require('fs');

// Se chalk non e' installato, modificare queste righe in console.log(message)
let debugMessage0 = (message) => console.log(chalk.white.bgBlue(message));
let debugMessage1 = (message) => console.log(chalk.cyan(message));
let debugMessage2 = (message) => console.log(chalk.magenta(message));
let debugMessage3 = (message) => console.log(chalk.white.bgBlack(message));
let errorMessage = (message) => console.log(chalk.white.bgRed.bold(message));

(async () => {

	// Dichiarazione variabili
	const userAgent = 'ua here';
  		
	let gotoUrl = 'https://www.politico.com/election-results/2019/mississippi/';

	const browser = await puppeteer.launch();
	const page = await browser.newPage();
	
	await page.setUserAgent(userAgent);
	await page.setRequestInterception(true);
	await page.setDefaultTimeout(180000);
	// https://github.com/GoogleChrome/puppeteer/issues/1599
	await page._client.send('Network.enable', {
		maxResourceBufferSize: 1024 * 1204 * 50,
		maxTotalBufferSize: 1024 * 1204 * 100,
	});
    
	// Settaggio dell'intercettazione delle richieste
	page.on('request', req => { req.continue(); });
	
	page.on('response', async (resp) => {
		let req = resp.request();
		
		if (req.url().endsWith('county.csv')) {
			debugMessage3('Richiesta catturata \t county.csv');
		
			resp.text()
				.then((text) => {
					if (text.length > 0) {
						// Salvo la risposta alla richiesta che mi interessa (quella che contiene i dati)
						let currentDate = new Date(),
							filenameOut = 'county_' + 
								currentDate.toISOString().split('.')[0].replace('T', '_').replace(/:/g, '').replace(/-/g, '') + 
								'.csv';
								
						fs.writeFile(
							'data/' + filenameOut, 
							text, 
							(err) => { 
								if (err) { 
									errorMessage('errore fs.writeFile()'); 
									errorMessage(err); 
									process.exit(1);
								}	
							}
						);
						debugMessage1('\tFile salvato');
					}
				})
				.catch((err) => { 
					errorMessage('errore resp.text()'); 
					errorMessage(err); 
					process.exit(1);
				});
		}
	});	
	
	await page.goto(gotoUrl);
	await page.waitForNavigation();
	
})();
