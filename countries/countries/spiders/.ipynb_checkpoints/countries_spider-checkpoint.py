import scrapy

class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['www.worldometers.info']
    start_urls = ['https://www.worldometers.info/world-population/']
    
    def parse(self, response):
        #traer todos los enlances a los paises
        countries = response.xpath('//td/a')
        
        #Recorrer todos los enlances
        for country in countries:
            name = country.xpath('.//text()').get()
            
            #me traigo el enlace, en este momento estoy parada en 
            # '//td/a' siempre de los siempres el href me da los enlaces
            link = country.xpath('.//@href').get()
            
            #para hacer llamdas se usa el yield
            yield response.follow(url = link,
                                  callback = self.parse_country,
                                  meta = {'country_name':name}
                                 )
    def parse_country(self, response):
        name = response.request.meta['country_name']
        rows = response.xpath("(//table[@class='table table-striped table-bordered table-hover table-condensed table-list'])[1]/tbody/tr")
        for row in rows:
            year = row.xpath(".//td[1]/text()").get()
            population = row.xpath(".//td[2]/strong/text()").get()
            migrants = row.xpath(".//td[5]/text()").get()
            
            #bloque para exportar
            yield{
                'country_name': name,
                'year': year,
                'population': population,
                'migrants': migrants
                }