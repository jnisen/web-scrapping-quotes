from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup

class Quotes(Item):
    quote = Field()
    author = Field()
    tags = Field()
    page = Field()

class quotesCrawler(CrawlSpider):
    name = 'quotes'

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 11
    }

    allowed_domains = ['quotes.toscrape.com']

    start_urls = ['https://quotes.toscrape.com/']

    download_delay = 1

    rules = (
        Rule(
            LinkExtractor(
                allow=(r'/page/\d*',),
                restrict_xpaths=('//li[contains(@class,"next")] | //li[contains(@class,"prev")]',)
            ), follow=True, callback='parse_quotes'),
    )


    def parse_quotes(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')

        quotes = soup.find_all('span', class_='text')
        authors = soup.find_all('small', class_='author')

        div_tags = soup.find_all('div', class_='tags')
        a_tags = [div.find_all('a', class_='tag') for div in div_tags]

        for quote, author, a_tag in zip(quotes, authors, a_tags):
            item = ItemLoader(Quotes(), response)
            item.add_value('page', response.url.split('/')[4])
            item.add_value('quote', quote.get_text(strip=True))
            item.add_value('author', author.get_text(strip=True))
            item.add_value('tags', [tag.text for tag in a_tag])
            yield item.load_item()
