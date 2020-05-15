# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse


# class WangyiproSpiderMiddleware:
#     # Not all methods need to be defined. If a method is not defined,
#     # scrapy acts as if the spider middleware does not modify the
#     # passed objects.
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         # This method is used by Scrapy to create your spiders.
#         s = cls()
#         crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
#         return s
#
#     def process_spider_input(self, response, spider):
#         # Called for each response that goes through the spider
#         # middleware and into the spider.
#
#         # Should return None or raise an exception.
#         return None
#
#     def process_spider_output(self, response, result, spider):
#         # Called with the results returned from the Spider, after
#         # it has processed the response.
#
#         # Must return an iterable of Request, dict or Item objects.
#         for i in result:
#             yield i
#
#     def process_spider_exception(self, response, exception, spider):
#         # Called when a spider or process_spider_input() method
#         # (from other spider middleware) raises an exception.
#
#         # Should return either None or an iterable of Request, dict
#         # or Item objects.
#         pass
#
#     def process_start_requests(self, start_requests, spider):
#         # Called with the start requests of the spider, and works
#         # similarly to the process_spider_output() method, except
#         # that it doesn’t have a response associated.
#
#         # Must return only requests (not items).
#         for r in start_requests:
#             yield r
#
#     def spider_opened(self, spider):
#         spider.logger.info('Spider opened: %s' % spider.name)


class WangyiproDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    # @classmethod
    # def from_crawler(cls, crawler):
    #     # This method is used by Scrapy to create your spiders.
    #     s = cls()
    #     crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
    #     return s

    def process_request(self, request, spider):
            # Called for each request that goes through the downloader
            # middleware.

            # Must either:
            # - return None: continue processing this request
            # - or return a Response object
            # - or return a Request object
            # - or raise IgnoreRequest: process_exception() methods of
            #   installed downloader middleware will be called
            return None

        # 通过该方法拦截五大板块对应的响应对象，进行篡改（将不满足需求的篡改为符合需求的）
        # 每拦截到一个响应对象，该方法就调用一次
    def process_response(self, request, response, spider):
            # 可以拦截到所有的响应对象，这里挑选出指定的响应对象进行篡改
            # 通过url指定request，通过request指定response。request对应唯一的response
            # spider是爬虫对象，表示爬虫类中的对象（wangyi.py中的spider）所以spider.modules_url可直接获取wangyi.py中的属性
            bro = spider.bro  # 获取了在爬虫类中定义的浏览器对象
            if request.url in spider.models_url:
                # rsponse  #五大板块对应的响应对象
                # 则很难对定位到的这些response进行篡改
                # 实例化一个新的响应对象（符合需求的：包含动态加载出的新闻数据，将新的响应对象替换原来旧的不满足需求的响应对象）
                # 如何获取动态加载出的响应数据呢？
                # 基于selenium是很便捷获取动态加载数据（步骤：1.实例化浏览器对象（实例化1次就好）并加载驱动程序）
                bro.get(request.url)  # 5个板块对应的url请求
                page_text = bro.page_source  # 页面源码数据，包含了动态加载的新闻数据
                new_response = HtmlResponse(url=request.url, body=page_text, encoding='utf-8', request=request)
                return new_response
            else:
                # response #其他请求（起始url所包含的响应对象）所对应的响应对象
                return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
