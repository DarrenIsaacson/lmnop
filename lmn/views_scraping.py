from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from Scraping.Scraping.spiders.show_spider import ShowSpider
from django.shortcuts import render
from scrapy.utils.log import configure_logging




def scrape(request):
	#check for logout session variable to display message
    try:
        configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
        runner = CrawlerRunner()
        
        r = runner.crawl(ShowSpider)
        r.addBoth(lambda _: reactor.stop())
        reactor.run()
    except Exception as e:
        print('\n ERROR:')
        print(e.args)
    return render(request, 'lmn/home.html')



