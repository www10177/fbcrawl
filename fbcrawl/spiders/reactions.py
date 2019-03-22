import scrapy

from scrapy.loader import ItemLoader
from fbcrawl.spiders.fbcrawl import FacebookSpider
from fbcrawl.items import ReactionItem
from parse import *

def page_formatter(url):
    if url.find('https://www.facebook.com/') != -1:
        return url[24:]
    elif url.find('https://mbasic.facebook.com/') != -1:
        return url[27:]
    elif url.find('https://m.facebook.com/') != -1:
        return url[22:]

class ReactionSpider(FacebookSpider):
    """
    Parse FB Reacion, given a post (needs credentials)
    """    
    name = "reactions"
    custom_settings = {
        'FEED_EXPORT_FIELDS': ['reaction_to','source','reaction','profile'],
        'DUPEFILTER_CLASS' : 'scrapy.dupefilters.BaseDupeFilter',
        'CONCURRENT_REQUESTS':1, 
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)

    def parse_page(self, response):
        '''
        parse page does multiple things:
            (1) load reaction list from post link
        '''
        #loads reaction list
        path = './/div[starts-with(@id,"sentence")]/a/@href'
        ans = response.xpath(path).extract()
        if len(ans) <1 :
            return
        ans = response.urljoin(ans[0])
        return scrapy.Request(ans,
                             callback=self.parse_reaction,
                             meta={'reaction_to':page_formatter(response.url),
                                   'flag':'init',
                                   'index':0})

    def parse_reaction(self,response):
        # parse all reaction list in this page
        path = '//table//li/table/tbody/tr/td[@class]/table/tbody/tr'
        for reaction in response.xpath(path):
            new = ItemLoader(item=ReactionItem(),selector=reaction)
            new.context['lang']=self.lang
            new.add_value('reaction_to',response.meta['reaction_to'])
            new.add_xpath('source','./td[3]//a/text()')  
            new.add_xpath('reaction','./td[2]//img/@alt')
            new.add_xpath('profile','./td[3]//a/@href')
            yield new.load_item()

        # go to next page
        next_path = '//span[text()="Vedi altri"]/../../a/@href'
        if response.xpath(next_path):
            url = response.xpath(next_path).extract()[0]
            parser=parse("{}/?limit={}&{}",url)
            url = "%s/?limit=%d&%s"%(url[0],100,url[2])

            self.logger.info("Going to next page %d " %(response.meta['index']+1))
            url = "https://mbasic.facebook.com"+url
            meta= response.meta
            meta['index']=meta['index']+1
            yield scrapy.Request(url,callback=self.parse_reaction,
                                    meta = meta)

        


