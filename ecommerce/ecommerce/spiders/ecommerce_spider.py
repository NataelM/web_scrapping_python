import scrapy

class EcommerceSpider(scrapy.Spider):
    name = 'products'
    allowed_domains = ['webscraper.io']
    start_urls = ['https://webscraper.io/test-sites/e-commerce/static/computers/laptops?page=1']

    def parse(self, response):
        products = response.xpath("//h4/a")
        for product in products:
            # los arrobas son atributos
            link = product.xpath("./@href").get()
            yield response.follow(url = link,
                                    callback = self.parse_product
                                    )
        #con esta parte vamos a la pagina siguiente
        next_page = response.xpath("//a[@rel='next']/@href").get()
        if next_page:
            yield response.follow(url = "https://webscraper.io" + next_page, 
                                 callback = self.parse
                                 )
    
    def parse_product(self, response):
        price = response.xpath("//h4[1]/text()").get()
        name = response.xpath("//h4[2]/text()").get()
        description = response.xpath("//p[@class='description']/text()").get()
        yield {
            'name': name,
            'price': price,
            'description': description
        }
