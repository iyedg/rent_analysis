# -*- coding: utf-8 -*-
import scrapy
from scrapy.shell import inspect_response
from rent_analysis.items import RentAnalysisItem
from functools import partial
from bs4 import BeautifulSoup as bs


class TunannSpider(scrapy.Spider):
    name = 'tunann'
    allowed_domains = ['www.tunisie-annonce.com']
    start_url = 'http://www.tunisie-annonce.com/AnnoncesImmobilier.asp'

    def start_requests(self):
        return [
            scrapy.Request(
                url=self.start_url, callback=self.pagination_parser)
        ]

    def pagination_parser(self, response):
        rows = response.css("tr.Tableau1")
        for row in rows:
            next_entry = row.css("td:nth-child(8) a::attr(href)").extract_first()
            if next_entry:
                next_entry = response.urljoin(next_entry)
                yield scrapy.Request(next_entry)
        next_page_link = response.xpath(
            "//img[@src='/images/n_next.gif']/parent::a/@href").extract_first()
        if next_page_link:
            next_page_link = response.urljoin(next_page_link)
            yield scrapy.Request(
                next_page_link, callback=self.pagination_parser)

    def parse(self, response):
        item = RentAnalysisItem()
        soup = bs(response.body, "lxml")
        inspect_response(response, self)
        def filter_tags(tag, col):                      
            """
                Return tags that are siblings to tags containing
                the specified column name in their string
            """
            return col in [i.string for i in tag.fetchPreviousSiblings()]

        category = partial(filter_tags, col="Catégorie")
        location = partial(filter_tags, col="Localisation")
        description = partial(filter_tags, col="Texte")
        address = partial(filter_tags, col="Adresse")
        area = partial(filter_tags, col="Surface")
        price = partial(filter_tags, col="Prix")
        created = partial(filter_tags, col="Insérée le")
        edited = partial(filter_tags, col="Modifiée le")


        if soup.find(category):
            item["category"] = soup.find(category).get_text()
        if soup.find(location):
            item["location"] = soup.find(location).get_text()
        if soup.find(description):
            item["description"] = soup.find(description).get_text()
        if soup.find(address):
            item["address"] = soup.find(address).get_text()
        if soup.find(area):
            item["area"] = soup.find(area).get_text()
        if soup.find(price):
            item["price"] = soup.find(price).get_text()
        if soup.find(created):
            item["created"] = soup.find(created).get_text()
        if soup.find(edited):
            item["edited"] = soup.find(edited).get_text()

        yield item
