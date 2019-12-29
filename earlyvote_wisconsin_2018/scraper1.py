import scrapy, json

class WiAbsScraper(scrapy.Spider):
	name = 'WiAbsScraper'

	dict_months = {'January':'1', 'February':'2', 'March':'3', 'April':'4', 'May':'5', 'June':'6', 
			'July':'7', 'August':'8', 'September':'9', 'October':'10', 'November':'11', 'December':'12'}

	start_urls = ['https://elections.wi.gov/publications/statistics/absentee',
					'https://elections.wi.gov/publications/statistics/absentee?page=1',
					'https://elections.wi.gov/publications/statistics/absentee?page=2']

	def parse(self, response):
		xpath_link_report = '//td[@class="views-field views-field-title"]/a/@href'

		for elem in response.xpath(xpath_link_report):
			url_report = 'https://elections.wi.gov' + elem.extract()
			yield scrapy.Request(url=url_report, callback=self.parse_report)
		
	def parse_report(self, response):
		xpath_date = '//div[@id="content-area"]//span[@class="date-display-single"]/text()'
		xpath_tr = '//div[@id="content-area"]//table[last()]/tbody/tr'
		
		# parsing the report's date
		date_report = response.xpath(xpath_date).extract_first()
		date_report = date_report.replace(',', '')
		
		for month, num in self.dict_months.items():
			date_report = date_report.replace(month, num)
			
		date_report = [int(i.strip()) for i in date_report.split(' ')]
		
		# extract data
		for row in response.xpath(xpath_tr)[1:]:
			list_td = row.xpath('td//text()').extract()
			list_td = filter(lambda d: d.strip() != '', list_td)
			
			county_name = list_td[0].lower().replace('county', '').strip()
			number_sent = int(list_td[1])
			number_returned = int(list_td[2])
			
			if 'total' in county_name or type(date_report[0]) == 'str':
				continue
			
			yield {'date': '/'.join([str(date_report[i]) for i in [2, 0, 1]]), 
					'year': date_report[2], 'month': date_report[0], 'day': date_report[1],
					'county': county_name, 'sent': number_sent, 'returned': number_returned}
