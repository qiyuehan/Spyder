# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from WangyiPro.items import WangyiproItem
class WangyiSpider(scrapy.Spider):
    name = 'Wangyi'
    allowed_domains = ['news.163.com']
    start_urls = ['https://news.163.com/']
    models_url = []

    def __init__(self):
        webdriver_path = r"G:\software\chrome_driver\chromedriver.exe"
        # 实例化一个有可视界面的谷歌浏览器对象,结合selenium使用处理动态网页数据
        self.bro = webdriver.Chrome(executable_path=webdriver_path)

        # 解析5大板块对应的详情页url
    def parse(self, response):
        # 首先先取出所有的<li>标签://*[@id="index2016_wrap"]/div[1]/div[2]/div[2]/div[2]/div[2]/div
        li_list = response.xpath('//*[@id="index2016_wrap"]/div[1]/div[2]/div[2]/div[2]/div[2]/div/ul/li')
        # 从li_list取出指定（所需要的）标签
        alist = [3, 4, 6, 7, 8]
        for index in alist:
            # 详情页的url
            model_url = li_list[index].xpath('./a/@href').get()
            self.models_url.append(model_url)

        # 依次对每个板块对应的页面进行请求
        for url in self.models_url:  # 对每个板块的url进行请求发送
            yield scrapy.Request(url, callback=self.parse_model)

        # 每一个板块对应的新闻标题相关的内容都是动态加载出来的，直接使用response.xpath()是解析不出来的，
        # 要使用下载中间件
    def parse_model(self, response):  # 解析每一个板块页面中对应新闻的标题和新闻详情页的url
        # 拿到了新的响应对象
        div_list = response.xpath('/html/body/div[1]/div[3]/div[4]/div[1]/div/div/ul/li/div/div')
        for div in div_list:
            title = div.xpath('./div/div[1]/h3/a/text').get()
            #获取新闻详情页的链接
            new_detail_url = div.xpath('./div/div[1]/h3/a/@href').get()
            item = WangyiproItem()
            item['title'] = title
            # 对新闻详情页的url发起请求，抓取新闻(meta是要发给parse_url的数据）
            yield scrapy.Request(url=new_detail_url, callback=self.parse_detail, meta={'item': item})

    def parse_detail(self, respone):  # 解析新闻内容的
        content = respone.xpath('//*[@id="endText"]//text()').getall()  # 获取所有的内容
        content = ''.join(content)  # 拿到新闻内容
        item = respone.meta['item']  # 接收发送的meta
        item['content'] = content  # 将content放进去

        # 提交到管道进行持久化存储
        yield item

    def closed(self, spider):
        self.bro.quit()  # 关闭浏览器


