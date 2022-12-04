import csv
import time
import random
from lxml import etree
from req import session

class cnvdSpider():
    def __init__(self):
        self.baseurl = "https://www.cnvd.org.cn/flaw/list"
        self.maxOffset = 17904
        self.headers = {
            'User-Agent': 'User-Agent:Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;'
        }
        self.session = session
        self.run()
        pass

    def run(self):
        data_list = []
        # 所有页
        for offset_value in range(0, self.maxOffset, 10):
            try:
                purse_time = random.uniform(8, 20)
                print(purse_time)
                print('purse_time: {}'.format(purse_time))
                time.sleep(purse_time)
                url = self.baseurl + "/?offset={}".format(str(offset_value))
                response = self.session.post(url, timeout=90, headers=self.headers, verify=False)
                print('URL:' + url +' ，状态码：{}'.format(response.status_code))
                tree = etree.HTML(response.text)
                # 遍历目录页URL
                for a_link in range(1, 11):
                    pages_url = tree.xpath("/html/body/div[4]/div[1]/div/div[1]/table//tr[{}]/td[1]/a/@href".format(a_link))
                    # 详情页
                    for url in pages_url:
                        data = {}
                        detail_url = 'https://www.cnvd.org.cn' + url

                        time.sleep(purse_time)
                        response = self.session.post(detail_url, timeout=90, headers=self.headers, verify=False)
                        print('detail_url:' + url + ' ，状态码：{}'.format(response.status_code))

                        cndv_detail_html = etree.HTML(response.content.decode("utf-8"))
                        title = cndv_detail_html.xpath("/html/body/div[4]/div[1]/div[1]/div[1]/h1/text()")[0].strip()
                        cnvd_id = cndv_detail_html.xpath(
                            "/html/body/div[4]/div[1]/div[1]/div[1]/div[2]/div[1]/table/tbody/tr[1]/td[2]/text()")[0].strip()
                        public_time = cndv_detail_html.xpath(
                            "/html/body/div[4]/div[1]/div[1]/div[1]/div[2]/div[1]/table/tbody/tr[2]/td[2]/text()")[0].strip()
                        level = cndv_detail_html.xpath(
                             "/html/body/div[4]/div[1]/div[1]/div[1]/div[2]/div[1]/table/tbody/tr[3]/td[2]/text()")
                        affect_products = cndv_detail_html.xpath(
                            "/html/body/div[4]/div[1]/div[1]/div[1]/div[2]/div[1]/table/tbody/tr[4]/td[2]/text()")[0].strip()

                        # 有的页面有，有的页面没
                        try:
                            cnv_id = cndv_detail_html.xpath(
                                "/html/body/div[4]/div[1]/div[1]/div[1]/div[2]/div[1]/table/tbody/tr[5]/td[2]/a/@href")[0]
                            i = 1
                        except Exception as e:
                            i = 0
                            continue

                        describe1 = cndv_detail_html.xpath(
                            "/html/body/div[4]/div[1]/div[1]/div[1]/div[2]/div[1]/table/tbody/tr[{}]/td[2]/text()".format(5+i))[0].strip()
                        describe2 = cndv_detail_html.xpath(
                            "/html/body/div[4]/div[1]/div[1]/div[1]/div[2]/div[1]/table/tbody/tr[{}]/td[2]/text()".format(5+i))[2].strip()

                        type = cndv_detail_html.xpath(
                            "/html/body/div[4]/div[1]/div[1]/div[1]/div[2]/div[1]/table/tbody/tr[{}]/td[2]/text()".format(6+i))[0].strip()
                        reference_link = cndv_detail_html.xpath(
                            "/html/body/div[4]/div[1]/div[1]/div[1]/div[2]/div[1]/table/tbody/tr[{}]/td[2]/text()".format(7+i))[0].strip()
                        cndv_solve_plan = cndv_detail_html.xpath(
                            "/html/body/div[4]/div[1]/div[1]/div[1]/div[2]/div[1]/table/tbody/tr[{}]/td[2]/text()".format(8+i))
                        manufacturer_patch = cndv_detail_html.xpath(
                            "/html/body/div[4]/div[1]/div[1]/div[1]/div[2]/div[1]/table/tbody/tr[{}]/td[2]/a/@href".format(9+i))[0]
                        verification = cndv_detail_html.xpath(
                            "/html/body/div[4]/div[1]/div[1]/div[1]/div[2]/div[1]/table/tbody/tr[{}]/td[2]/text()".format(10+i))[0].strip()
                        report_time = cndv_detail_html.xpath(
                            "/html/body/div[4]/div[1]/div[1]/div[1]/div[2]/div[1]/table/tbody/tr[{}]/td[2]/text()".format(11+i))[0].strip()
                        collect_time = cndv_detail_html.xpath(
                            "/html/body/div[4]/div[1]/div[1]/div[1]/div[2]/div[1]/table/tbody/tr[{}]/td[2]/text()".format(12+i))[0].strip()
                        update_time = cndv_detail_html.xpath(
                            "/html/body/div[4]/div[1]/div[1]/div[1]/div[2]/div[1]/table/tbody/tr[{}]/td[2]/text()".format(13+i))[0].strip()
                        attachment = cndv_detail_html.xpath(
                            "/html/body/div[4]/div[1]/div[1]/div[1]/div[2]/div[1]/table/tbody/tr[{}]/td[2]/text()".format(14+i))[0].strip()

                        data["漏洞标题"] = title
                        data["CNVD-ID"] = cnvd_id
                        data["公开日期"] = public_time
                        data["危害级别"] = level
                        data["影响产品"] = affect_products
                        data["CVE-ID"] = cnv_id
                        data["漏洞描述"] = describe1 + describe2
                        data["漏洞类型"] = type
                        data["参考链接"] = reference_link
                        data["漏洞解决方案"] = cndv_solve_plan
                        data["厂商补丁"] = 'https://www.cnvd.org.cn' + manufacturer_patch
                        data["验证信息"] = verification
                        data["报送时间"] = report_time
                        data["收录时间"] = collect_time
                        data["更新时间"] = update_time
                        data["漏洞附件"] = attachment
                        data_list.append(data)
                        print(data)

                        f = open ('data/Cndv1.csv','w', encoding='utf-8-sig', newline='') #newline=''防止空行
                        csv_write = csv.writer(f)
                        csv_write.writerow(['漏洞标题','CNVD-ID','公开日期','危害级别','影响产品','CVE-ID','漏洞描述','漏洞类型','参考链接','漏洞解决方案','厂商补丁','验证信息','报送时间','收录时间','更新时间','漏洞附件'])
                        for data in data_list:
                            csv_write.writerow([data["漏洞标题"],data["CNVD-ID"],data["公开日期"],data["危害级别"],data["影响产品"],data["CVE-ID"],data["漏洞描述"],data["漏洞类型"],data["参考链接"],data["漏洞解决方案"],data["厂商补丁"],data["验证信息"],data["报送时间"],data["收录时间"],data["更新时间"],data["漏洞附件"]])
                        print("第{}页 第{}条 爬取结束".format(str(int(offset_value / 10) + 1), str(a_link)))
                        pass
                pass
            except Exception as e:
                print(e)
                print("读取{}页时发生异常~~ [跳过]".format(str(int(offset_value / 10))))
                pass
        pass

if __name__ == '__main__':
    cnvdSpider()