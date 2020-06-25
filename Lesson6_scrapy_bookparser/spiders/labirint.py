# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem


class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/%D0%B1%D1%83%D1%85%D0%B3%D0%B0%D0%BB%D1%82%D0%B5%D1%80%D0%B8%D1%8F']

    def parse(self, response: HtmlResponse):
        next_page = response.css('a.pagination-next__text::attr(href)').extract_first()
        books_links = response.css('a.product-title-link::attr(href)').extract()
        for link in books_links:
            yield response.follow(link, callback=self.book_parse)
        yield response.follow(next_page, callback=self.parse)

    def book_parse(self, response: HtmlResponse):
        book_link = response.url
        name = response.xpath("//div[@id='product-title']/h1/text()").extract_first()
        author = response.xpath("//div[@class='authors']/a/text()").extract_first()
        wo_bonus_price = response.xpath("//span[@class='buying-priceold-val-number']/text()").extract_first()
        bonus_price = response.xpath("//span[@class='buying-pricenew-val-number']/text()").extract_first()
        no_bonus_price = response.xpath("//span[@class='buying-price-val-number']/text()").extract_first()
        rate = response.xpath("//div[@id='rate']/text()").extract_first()
        yield BookparserItem(name=name, author=author, book_link=book_link, wo_bonus_price=wo_bonus_price, bonus_price=bonus_price, no_bonus_price=no_bonus_price, rate=rate)
