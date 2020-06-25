# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem


class Book24Spider(scrapy.Spider):
    name = 'book24'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/search/?q=%D0%B1%D1%83%D1%85%D0%B3%D0%B0%D0%BB%D1%82%D0%B5%D1%80%D0%B8%D1%8F']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@class='catalog-pagination__item _text js-pagination-catalog-item']/@href").extract_first()
        books_links = response.xpath("//div[@class='catalog-products__item js-catalog-products-item']//a[@class='book__image-link js-item-element ddl_product_link']/@href").extract()
        for link in books_links:
            yield response.follow(link, callback=self.book_parse)
        yield response.follow(next_page, callback=self.parse)

    def book_parse(self, response: HtmlResponse):
        book_link = response.url
        name = response.xpath("//h1[@class='item-detail__title']/text()").extract_first()
        author = response.xpath("//a[@class='item-tab__chars-link js-data-link']/text()").extract_first()
        wo_bonus_price = response.xpath("//div[@class='item-actions__price-old']/text()").extract_first()
        bonus_price = no_bonus_price = response.xpath("//div[@class='item-actions__price']/text()").extract_first()
        rate = response.xpath("//div[@class='live-lib__rate-value']/text()").extract_first()
        yield BookparserItem(name=name, author=author, book_link=book_link, wo_bonus_price=wo_bonus_price, bonus_price=bonus_price, no_bonus_price=no_bonus_price, rate=rate)
