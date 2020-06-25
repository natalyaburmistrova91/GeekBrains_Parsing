import scrapy
from scrapy.http import HtmlResponse
from shopparser.items import ShopparserItem
from scrapy.loader import ItemLoader

class LeroymerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, search):
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}&family=790fa8b0-70bd-11e9-afe4-db26cf073c46&suggest=true']

    def parse(self, response):
        next_page = response.xpath("//div[@class='next-paginator-button-wrapper']/a/@href").extract_first()
        good_links = response.xpath("//div[@class='plp-card-list-inner clearfix']//div[@class='ui-product-card']/@data-product-url").extract()
        for link in good_links:
            yield response.follow(link, callback=self.good_parse)
        yield response.follow(next_page, callback=self.parse)

    def good_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=ShopparserItem(), response=response)
        loader.add_xpath('photos', "//picture[@slot='pictures']/source[@media=' only screen and (min-width: 1024px)']/@srcset")
        loader.add_xpath('name', "//h1[@slot='title']/text()")
        loader.add_value('link', response.url)
        loader.add_xpath('price', "//span[@slot='price']/text()")
        params = {}
        params_block = response.xpath("//div[@class='def-list__group']")
        for p in params_block:
            p_name = p.xpath(".//dt[@class='def-list__term']/text()").extract_first()
            p_value = p.xpath(".//dd[@class='def-list__definition']/text()").extract_first()
            params[p_name] = p_value
        loader.add_value('params', params)
        yield loader.load_item()
        # photos = response.xpath("//picture[@slot='pictures']/source[@media=' only screen and (min-width: 1024px)']/@srcset").extract()
        # name = response.xpath("//h1[@slot='title']/text()").extract_first()
        # link = response.url
        # price = response.xpath("//span[@slot='price']/text()").extract_first()
        # yield ShopparserItem(name=name, photos=photos, link=link, price=price,
        #                      params=params)
