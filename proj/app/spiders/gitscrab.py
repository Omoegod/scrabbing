from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from app.items import Repositories


class GitscrabSpider(CrawlSpider):
    name = 'gitscrab'
    allowed_domains = ['github.com']
    start_urls = ['https://github.com/scrapy'] #None

    rules = [
        Rule(LinkExtractor(restrict_xpaths=('//*[@id="js-pjax-container"]/div/header/div[2]/nav/div/ul/li[2]/a'),), follow=True),
        Rule(LinkExtractor(restrict_xpaths=('//*[@id="org-repositories"]/div/div/div[1]/ul/li/div/div[1]/div[1]/h3/a'),), callback='parse', follow=True),
    ]

    def parse(self, response): 
        
        item = Repositories()
        item['rep_url'] = response.url
        item['username'] = response.xpath('//*[@id="repository-container-header"]/div[1]/div/div/span[1]/a/text()').get()
        item['rep_name'] = response.xpath('//*[@id="repository-container-header"]/div[1]/div/div/strong/a/text()').get()
        item['description'] = " ".join(response.xpath('//*[@id="repo-content-pjax-container"]/div/div/div[3]/div[2]/div/div[1]/div/p//text()').getall()).replace("\n","").strip()
        item['stars'] = response.xpath('//*[@id="repo-stars-counter-star"]/@title').get()
        item['forks'] = response.xpath('//*[@id="repo-network-counter"]/@title').get()
        item['watching'] = response.xpath('//*[@id="repo-content-pjax-container"]/div/div/div[3]/div[2]/div/div[1]/div/div[7]/a/strong/text()').get()
        item['url'] = response.xpath('//*[@id="repo-content-pjax-container"]/div/div/div[3]/div[2]/div/div[1]/div/div[1]/span/a/@href').get()
        item['commits'] = response.xpath('//*[@id="repo-content-pjax-container"]/div/div/div[3]/div[1]/div[2]/div[1]/div/div[4]/ul/li/a/span/strong/text()').get()
        item['author_commit'] =  response.xpath('//*[@id="repo-content-pjax-container"]/div/div/div[3]/div[1]/div[2]/div[1]/div/div[2]/div[1]/a/text()').get()
        item['name_commit'] = ''.join(str(response.xpath('//*[@id="repo-content-pjax-container"]/div/div/div[3]/div[1]/div[2]/div[1]/div/div[2]/div[1]/span/a[1]/@title').get()).split('\n'))
        item['datetime_commit'] = response.xpath('//*[@id="repo-content-pjax-container"]/div/div/div[3]/div[1]/div[2]/div[1]/div/div[2]/div[2]/a[2]/relative-time/@datetime').get()
        item['releases'] = response.xpath('//*[@id="repo-content-pjax-container"]/div/div/div[3]/div[2]/div/div[2]/div/h2/a/span/text()').get()
        item['version_releases'] = response.xpath('//*[@id="repo-content-pjax-container"]/div/div/div[3]/div[2]/div/div[2]/div/a/div/div[1]/span[1]/text()').get()
        item['datetime_releases'] = response.xpath('//*[@id="repo-content-pjax-container"]/div/div/div[3]/div[2]/div/div[2]/div/a/div/div[2]/relative-time/@datetime').get()
        url_relaise = response.xpath('//*[@id="repo-content-pjax-container"]/div/div/div[3]/div[2]/div/div[2]/div/h2/a/@href').get()  
        return response.follow(url_relaise, self.parse_changlog, cb_kwargs=dict(item=item))

    def parse_changlog(self, response, item):
        
        item['changelog_releases'] = " ".join(response.xpath('//*[@id="repo-content-pjax-container"]/div/div[2]/div[1]/div[2]/div/div[1]/div[4]//text()').getall()).replace("\n","")
        yield item 
        