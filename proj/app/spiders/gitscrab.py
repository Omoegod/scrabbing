import collections
import scrapy
from scrapy.item import Item, Field
from app.items import Repositories
from urllib.parse import urljoin

from pymongo import MongoClient

client = MongoClient()
db = client.gitscrab
collections = db.collections



class GitscrabSpider(scrapy.Spider):
    name = 'gitscrab'
    
    start_urls = ['https://github.com/scrapy',]
                  #'https://github.com/celery']

    def parse(self, response):

        for repos_list_link in response.xpath(
           '//*[@id="js-pjax-container"]/div/header/div[2]/nav/div/ul/li[2]/a/@href').getall():
            url = urljoin(response.url, repos_list_link)
            #print(url)
            yield response.follow(url)
            
            for repos_link in response.xpath('//*[@id="org-repositories"]/div/div/div[1]/ul/li/div/div[1]/div[1]/h3/a/@href').getall():
                url = urljoin(response.url, repos_link)
                #print(url)
                yield response.follow(url, callback = self.parse_repo)  
                


    def parse_repo(self, response):

        item = Repositories()
        rep_name = str(response.xpath('//*[@id="repository-container-header"]/div[1]/div/h1/strong/a/text()').get()).strip()    
        item['rep_name'] = rep_name
        description = str(response.xpath('//*[@id="repo-content-pjax-container"]/div/div[3]/div[2]/div/div[1]/div/p/text()').get()).strip()
        item['description'] = description
        url = response.xpath('//*[@id="repo-content-pjax-container"]/div/div[3]/div[2]/div/div[1]/div/div[1]/span/a/@href').get()
        item['url'] = url
        stars = response.xpath('//*[@id="repo-content-pjax-container"]/div/div[3]/div[2]/div/div[1]/div/div[6]/a/strong/text()').get()
        item['stars'] = stars
        forks = response.xpath('//*[@id="repo-content-pjax-container"]/div/div[3]/div[2]/div/div[1]/div/div[8]/a/strong/text()').get()
        item['forks'] = forks
        watching = response.xpath('//*[@id="repo-content-pjax-container"]/div/div[3]/div[2]/div/div[1]/div/div[7]/a/strong/text()').get()
        item['watching'] = watching
        commits = response.xpath('//*[@id="repo-content-pjax-container"]/div/div[3]/div[1]/div[2]/div[1]/div/div[4]/ul/li/a/span/strong/text()').get()
        item['commits'] = commits
        author_commit =  response.xpath('//*[@id="repo-content-pjax-container"]/div/div[3]/div[1]/div[2]/div[1]/div/div[2]/div[1]/a/text()').get()
        name_commit = response.xpath('//*[@id="repo-content-pjax-container"]/div/div[3]/div[1]/div[2]/div[1]/div/div[2]/div[1]/span/a[1]/text()').get()
        datetime_commit = response.xpath('//*[@id="repo-content-pjax-container"]/div/div[3]/div[1]/div[2]/div[1]/div/div[2]/div[2]/a[2]/relative-time/@datetime').get()
        item['info_commit'] = author_commit, name_commit, datetime_commit
        releases = response.xpath('//*[@id="repo-content-pjax-container"]/div/div[3]/div[2]/div/div[2]/div/h2/a/span/text()').get()
        item['releases'] = releases
        
        def parse(response):
            
            version_releases = str(response.xpath('//*[@id="repo-content-pjax-container"]/div[2]/div[1]/div[2]/div/div[1]/div[2]/div[1]/h1/a/text()').get()).strip()
            datetime_releases = response.xpath('//*[@id="repo-content-pjax-container"]/div[2]/div[1]/div[1]/div[1]/local-time/@datetime').get()   
            changelog_releases = response.xpath('//*[@id="repo-content-pjax-container"]/div[2]/div[1]/div[2]/div/div[1]/div[4]//text()').getall()
            changelog_releases = " ".join(changelog_releases).replace("\n","")
            item['info_releases'] = version_releases, datetime_releases, changelog_releases 
            yield item

        collections.insert_one(dict(item))

        for url_releases in response.xpath('//*[@id="repo-content-pjax-container"]/div/div[3]/div[2]/div/div[2]/div/h2/a/@href').getall():
            url = urljoin(response.url, url_releases)
            #print(url)
            yield response.follow(url, callback = parse)    
           
   
        
    




