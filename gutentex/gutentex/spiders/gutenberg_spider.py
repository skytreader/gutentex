from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

class GutenbergSpider(CrawlSpider):
    
    name = "gutenberg.org"
    allowed_domains = ["gutenberg.org"]
    # Hard code for King Arthur for now...
    start_urls = ["http://www.gutenberg.org/ebooks/12753"]
    rules = [Rule(SgmlLinkExtractor(allow=["/ebooks/\d+"]), "parse_book_record")]

    def parse_book_record(self, response):
        self.log("Parsing %s", response.url)

        selector = HtmlXPathSelector(response)

        book = GutenbergItem()
        # But what if there are more than one h1s in the document?
        # Weird itemprop attribute in the gutenberg code.
        book["title"] = selector.select("//h1/text()").extract()
        book["links"] = selector.select("//a[@class='link']")
        print "HEY SOUL SISTER"
        return book
