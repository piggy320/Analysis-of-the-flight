#爬取同城旅游网机票信息
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from spider.comm.spider_communal import is_same_month
from selenium.webdriver.chrome.options import Options
import time
import re
from lxml import etree

'''
    date_str 查询日期
    start_city 查询起始城市
    arrive_city 查询抵达城市
'''
class MySpider():
    def __init__(self, date_str, start_city, arrive_city):
        self.date_str = date_str
        self.start_city = start_city
        self.arrive_city = arrive_city
        # self.driver = webdriver.Chrome()
        options = Options()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)
    '''
    通过selenium控制Chrome驱动，完成模拟人工输入查询地址和日期然后点击提交获取查询结果html的流程
    '''
    def get_query_results(self):

        self.driver.implicitly_wait(10)
        self.driver.get('https://www.ly.com/FlightQuery.aspx')
        locator = (By.ID, 'txtAirplaneCity1')
        try:
            # 显性等待
            WebDriverWait(self.driver, 20, 0.5).until(EC.presence_of_element_located(locator))
            # 起始地城市input元素获取并清空值，然后填入城市名称,输入之后模拟按回车键
            txtAirplaneCity1 = self.driver.find_elements_by_id("txtAirplaneCity1")[0]
            txtAirplaneCity1.clear()
            txtAirplaneCity1.send_keys(self.start_city)
            txtAirplaneCity1.send_keys(Keys.ENTER)
            # 抵达地城市input元素获取并清空值，然后填入城市名称，输入之后模拟按回车键
            txtAirplaneCity2 = self.driver.find_elements_by_id("txtAirplaneCity2")[0]
            txtAirplaneCity2.clear()
            txtAirplaneCity2.send_keys(self.arrive_city)
            txtAirplaneCity2.send_keys(Keys.ENTER)

            # 如果所查询的日期在当月范围内，则定位到日历插件中第1个div否则定位到第2个div，div1 表示当月，div2表示下一个月
            if is_same_month(self.date_str):
                # 定位到日历插件
                element_calendar = self.driver.find_elements_by_xpath(
                    "/html/body/div[17]/div/div[1]/div[1]/div/table/tbody/tr/td/span")
                for item in element_calendar:
                    if item.text == str(int(self.date_str.split("-")[2])):
                        item.click()
            else:
                element_calendar = self.driver.find_elements_by_xpath(
                    "/html/body/div[17]/div/div[1]/div[2]/div/table/tbody/tr/td/span")
                for item in element_calendar:
                    if item.text == str(int(self.date_str.split("-")[2])):
                        item.click()
            # 定位搜索按钮并模拟点击提交
            airplaneSubmit = self.driver.find_elements_by_id("airplaneSubmit")[0]
            airplaneSubmit.click()
            # 显性等待后，定位到机票查询结果div，然后获取div内的html
            locator_content = (By.ID, 'allFlightListDom_1')
            WebDriverWait(self.driver, 20, 0.5).until(EC.presence_of_element_located(locator_content))
            flight_list_html = self.get_flight_list_dom()
            # 返回结果
            data_list = []
            '''
            此处判断返回的flight_list_html里面是否包含有机票信息，如果有直接返回此html代码，否则使用for循环
            从新尝试10次，每循环一次暂停一秒
            '''
            if flight_list_html:
                for item in flight_list_html:
                    data_list.append(item.get_attribute('innerHTML'))
            else:
                for x in range(10):
                    flight_list_html = self.get_flight_list_dom()
                    if flight_list_html:
                        for item in flight_list_html:
                            data_list.append(item.get_attribute('innerHTML'))
                        break
                    time.sleep(1)
            return data_list

        except Exception as ex:
            print(ex)
        finally:
            self.driver.close()

    '''
    定位到机票查询结果div，然后获取div内的html
    '''

    def get_flight_list_dom(self):
        # 通过观察页面发现这个机票列表数据有三种格式，所以将它们都提取出来拼接成一个List返回
        flight_list_html_n = self.driver.find_elements_by_xpath(
            '//div[@class="clearfix flightList"]//div[@class="flist_box"]')
        flight_list_html_top = self.driver.find_elements_by_xpath(
            '//div[@class="clearfix flightList"]//div[@class="flist_box f_m_top flist_boxat"]')
        flight_list_html_boxbot = self.driver.find_elements_by_xpath(
            '//div[@class="clearfix flightList"]//div[@class="flist_box flist_boxbot"]')
        return flight_list_html_n + flight_list_html_top + flight_list_html_boxbot

    '''
    提取数据
    respone get_query_results()方法中返回的结果内容
    '''

    def extract(self, respone):
        try:
            data_list = []
            for item in respone:
                data = {}
                html = etree.HTML(item)
                # 航司
                airline = html.xpath('/html/body/table/tbody/tr/td[1]/div[1]/text()')
                data["airline"] = airline[0] if airline else ""
                # 航班号
                flight_number = re.findall("[a-zA-Z]{2}\d+", airline[0])
                data["flight_number"] = flight_number[0] if flight_number else ""
                # 出发时间
                dep_time = html.xpath('/html/body/table/tbody/tr/td[2]/div[1]/text()')
                data["dep_time"] = dep_time[0] if dep_time else ""
                # 出发机场
                dep_airport = html.xpath('/html/body/table/tbody/tr/td[2]/div[2]/text()')
                data["dep_airport"] = dep_airport[0] if dep_airport else ""
                # 飞机类型
                aircraft_type = html.xpath('/html/body/table/tbody/tr/td[1]/div[2]/a/text()')
                data["aircraft_type"] = aircraft_type[0] if aircraft_type else ""
                # 抵达时间
                arr_time = html.xpath('/html/body/table/tbody/tr/td[4]/div[1]/text()')
                data["arr_time"] = arr_time[0] if arr_time else ""
                # 抵达机场
                arr_airport = html.xpath('/html/body/table/tbody/tr/td[4]/div[2]/text()')
                data["arr_airport"] = arr_airport[0] if arr_airport else ""
                # 价格
                price = html.xpath('/html/body/table/tbody/tr/td[8]/div[1]/span[1]/em[1]/text()')
                data["price"] = price[0] if price else ""
                data_list.append(data)
            return data_list
        except Exception as ex:
            print(ex)
            return None


if __name__ == "__main__":
    my_spider = MySpider("2020-09-04", "成都", "北京")
    res = my_spider.get_query_results()
    data_list = my_spider.extract(res)
    for item in data_list:
        print(item)

