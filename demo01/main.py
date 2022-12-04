import time
from random import random
from req import session
from lxml import etree

class cnvdSpider():
    def __init__(self):
        self.baseurl = "https://www.cnvd.org.cn/flaw/list"
        self.maxOffset = 50
        self.headers = {
            'User-Agent': 'User-Agent:Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;'
        }
        self.proxies = {
            'http': 'localhost:6228'
        }
        self.session = session
        self.run()
        pass

    def run(self):
        for offset_value in range(0, self.maxOffset, 10):
            try:
                purse_time = random.uniform(2, 4)
                print('purse_time: {}'.format(purse_time))
                time.sleep(purse_time)

                # Requests.Post（）在调用完成后，即关闭连接，不保存cookies
                # Session.Post() 在调用后，保持会话连接，保存cookies
                url = self.baseurl + "/?offset={}".format(str(offset_value))
                response = self.session.post(url, timeout=5, headers=self.headers, proxies=self.proxies,verify=False,)

                tree = etree.HTML(response.text)
                for a_link in range(1, 11):
                    news_title = tree.xpath("/html/body/div[4]/div[1]/div/div[1]/table//tr[{}]/td[1]/a/text()".format(a_link))
                    for i in news_title:
                        print(i.strip())
                pass
            except Exception as e:
                print("读取{}页时发生异常~~ [跳过]".format(str(int(offset_value / 10))))
                pass
        pass

if __name__ == '__main__':
    cnvdSpider()