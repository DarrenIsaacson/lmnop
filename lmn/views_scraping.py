from scrapy.crawler import CrawlerProcess
from Scraping.spiders.show_spider import ShowSpider
from django.shortcuts import render



def scrape(request):
	#check for logout session variable to display message
    try:
        process = CrawlerProcess()
        process.crawl(ShowSpider)
        process.start()
    except Exception as e:
        print('\n ERROR:')
        print(e.args)
    return render(request, 'lmn/home.html')



