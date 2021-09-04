# -*- coding: utf-8 -*-
from functools import partial

import scrapy
from bs4 import BeautifulSoup as bs

from rent_analysis.items import RentAnalysisItem


class TunannSpider(scrapy.Spider):
    name = "tunann"
    allowed_domains = ["www.tunisie-annonce.com"]
    start_url = "http://www.tunisie-annonce.com/AnnoncesImmobilier.asp"

    def start_requests(self):
        return [scrapy.Request(url=self.start_url, callback=self.pagination_parser)]

    def pagination_parser(self, response):
        rows = response.css("tr.Tableau1")
        for row in rows:
            next_entry = row.css("td:nth-child(8) a::attr(href)").extract_first()
            if next_entry:
                next_entry = response.urljoin(next_entry)
                yield scrapy.Request(next_entry)
        next_page_link = response.xpath(
            "//img[@src='/images/n_next.gif']/parent::a/@href"
        ).extract_first()
        if next_page_link:
            next_page_link = response.urljoin(next_page_link)
            yield scrapy.Request(next_page_link, callback=self.pagination_parser)

    def parse(self, response):
        item = RentAnalysisItem()
        soup = bs(response.body, "lxml")
        item_columns = {
            "category": "Catégorie",
            "location": "Localisation",
            "description": "Texte",
            "address": "Adresse",
            "area": "Surface",
            "price": "Prix",
            "created": "Insérée le",
            "edited": "Modifiée le",
        }

        for item_attr, column_name in item_columns.items():
            try:
                item[item_attr] = soup.find(
                    partial(filter_tags, col=column_name)
                ).text.strip()
            except Exception:
                pass

        yield item


def filter_tags(tag, col):
    """
    Return tags that are siblings to tags containing
    the specified column name in their string
    """
    return col in [i.string for i in tag.fetchPreviousSiblings()]
