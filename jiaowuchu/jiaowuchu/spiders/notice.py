
import re
import requests
import scrapy
import time
from ..items import JiaowuchuItem

start = 0
limit = 100

def get_times(script):
    url = "https://jwch.fzu.edu.cn/system/resource/code/news/click/clicktimes.jsp"
    ans = re.split(r'[(,")]', script)
    params = {
        "wbnewsid": ans[1],
        "owner": ans[2],
        "type": "wbnewsfile",
        "randomid": "nattach"
    }
    return requests.get(url, params=params).json()['wbshowtimes']

class NoticeSpider(scrapy.Spider):
    name = "notice"
    # allowed_domains = ["xx"]
    #start_urls = ["https://xx"]
    
    def start_requests(self):
        home = 'https://jwch.fzu.edu.cn/jxtz.htm'
        yield scrapy.Request(home, callback=self.parse_list)

    def parse_list(self, response):
        global start
        notice_list = response.xpath('//ul[@class="list-gl"]/li')
        for span in notice_list:
            start += 1
            if start > limit:
                break
            yield response.follow(span.xpath('./a')[0], callback=self.parse_notice)
        else:
            next_page = response.xpath("//span[@class='p_next p_fun']/a")[0]
            yield response.follow(next_page, callback=self.parse_list)

    def parse_notice(self, response):
        result = JiaowuchuItem()
        try:
            result['section'] = response.xpath('//p[@class="w-main-dh-text"]/a[2]/text()').extract_first()
            result['title'] = response.xpath('//h4[@align="center"]/text()').extract_first()
            result['post_time'] = response.xpath('//span[@class="xl_sj_icon"]/text()')[0].re(r"\d{4}-\d{2}-\d{2}")[0]
            result['brief'] = response.xpath('//meta[@name="description"]/@content').extract_first()
            result['url'] = response.url
            result['content'] = '\n'.join([item.xpath('string(.)').get() for item in response.xpath('//div[@class="v_news_content"]/p')])
            attachment = response.xpath('//ul[@style="list-style-type:none;"]/li')
            result['attachment'] = [{
                "title": item.xpath('./a/text()').get(),
                "url": item.xpath('./a/@href').get(),
                "download_times": get_times(item.xpath('./span/script/text()').get())
            } for item in attachment]
        except Exception as e:
            self.logger.error(f"解析 {response.url} 出错: {e}")
        yield result
