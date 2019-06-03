import scrapy
import json
from urllib.request import urlopen
from bs4 import BeautifulSoup

class my_code(scrapy.Spider):

    name = "codeforces"
    allowed_domains = ['codeforces.com']

    MAX = 20
    count = MAX

    start_urls= [
            # 'https://codeforces.com/problemset/status/page/1?order=BY_ARRIVED_DESC',
            'http://codeforces.com/api/problemset.recentStatus?count=60',
        ]
    # custom_settings = {
    #     # 'DOWNLOAD_DELAY' : 1,
    #     # Configure maximum concurrent requests performed by Scrapy (default: 16)
    #     'CONCURRENT_REQUESTS' : 2,
    # }
    base_url = "https://codeforces.com"


    def parse(self, response):
        if response is None:
            print("oh,I have benn refused!")
            return
        html = response.text
        json_data = json.loads(html)
        for data in json_data['result']:
            problem_id = data['id']
            contest_id = data['contestId']
            lang = data['programmingLanguage']
            verdict = data['verdict']
            if verdict.find('OK') != -1 and lang.find('GNU') != -1:
                print(problem_id, contest_id, lang, verdict)
                source = urlopen('https://codeforces.com/problemset/submission/' +
                                 str(contest_id) + '/' + str(problem_id)).read().decode('utf-8')
                soup = BeautifulSoup(source, features='lxml')
                sub_txts = soup.find_all("pre", {"id": "program-source-text"})
                for sub_txt in sub_txts:
                    print(sub_txt.text)

        # urls = response.xpath("//a[@class='view-source']//@href").extract()
        # for url in urls:
        #     print(self.base_url + url + "\n")
        #     yield scrapy.Request(self.base_url + url,
        #                          meta={
        #                              'dont_redirect': True,
        #                              'handle_httpstatus_list': [302]
        #                          },
        #                          callback=self.get_source)
        #     break
        # next_count = int(self.start_urls[-1].split('/')[-1][0]) + 1
        # if next_count > 1:
        #     return
        # next_page = 'https://codeforces.com/problemset/status/page/' + str(next_count) + '?order=BY_ARRIVED_DESC'
        # self.start_urls.append(next_page)
        # yield scrapy.Request(next_page,callback=self.parse)

    def get_source(self,response):
        if response is None:
            print("oh,I have benn refused!")
            return
        # print(response.body)
        verdict = response.xpath("//span[@class='verdict-accepted']").extract()
        lang = response.xpath("//td[@class='bottom']//text()").extract()
        print(lang)
        title = response.xpath("//title//text()").extract_first()
        print(title)
        if len(verdict) > 0:
            print(response.xpath("//pre[@id='program-source-text']//text()").extract_first() + "\n")
        else:
            print("this is not a right answer")