import scrapy
from ..items import QuotescrapItem


class QuoteSpider(scrapy.Spider):
    name = 'quotes'
    page_number = 2

    start_urls = ['https://www.greatest-quotations.com/search/quotes-wisdom.html?page=1']

    def parse(self, response):
        all_divs =  response.css('[id^="q"]')
        items = QuotescrapItem()

        for quotes in all_divs:
            title = quotes.css('.fbquote::text').extract()
            author = quotes.css('.auteurfbnaam::text').extract()
            tags = 'wisdom'

            items['title'] = title
            items['author'] = author
            items['tags'] = tags

            yield items

        next_page = 'https://www.greatest-quotations.com/search/quotes-wisdom.html?page=' + str(QuoteSpider.page_number)

        if QuoteSpider.page_number < 25:
            QuoteSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)
