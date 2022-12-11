import scrapy

class BookSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
      books = response.xpath("//h3/a")
      for book in books:
          link = book.xpath(".//@href").get()
          yield response.follow(url=link, callback=self.parse_book)
      next_page = response.xpath("//li[@class='next']/a/@href").get()    
      if next_page:
           yield response.follow(url=next_page, callback=self.parse)

    def parse_book(self, response):
        title = response.xpath("//div[@class='col-sm-6 product_main']/h1/text()").get()
        section = response.xpath("//ul/li[3]/a/text()").get()
        price = response.xpath("//p[@class='price_color']/text()").get()
        description = response.xpath("//div[@id='product_description']/following-sibling::p/text()").get()
        availability = response.xpath("//th[contains(text(), 'Availability')]/following-sibling::td/text()").get()
        yield {
            'title': title,
            'section': section,
            'price': price,
            'description': description,
            'availability': availability
            }      