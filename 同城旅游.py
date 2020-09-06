import multiprocessing
from multiprocessing import Process
import time
import datetime
from lxml import etree#lxml:使用 xpath 定位元素来提取元素
#selenium:用于Web应用程序测试的工具
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import csv
# 机场代码列表
namelist= ["XMN","SHA","PKX","TSN", "HGH","XIY","SZX", "TAO","DLC", "WUH",
           "CTU","CAN","CKG","KWE","KMG","KHN","TNA","NKG","CGQ","CSX",
           "DYG","HAK","HRB","SJW","SHE"]
#{"XMN":"厦门","SHA":"上海","PKX":"北京","TSN": "天津"," HGH": "杭州", "XIY": "西安","SZX":"深圳","TAO":"青岛","DLC": "大连","WUH": "武汉",
#"CTU": "成都","CAN": "广州","CKG": "重庆","KWE":"贵阳","KMG":"昆明","KHN":"南昌","TNA":"济南","NKG":"南京","CGQ":"长春","CSX":"长沙",
  # "DYG":"张家界","HAK":"海口","HRB":"哈尔滨","SJW":"石家庄","SHE":"沈阳"}
 
# 现在的时间
now = datetime.datetime.now()
# 开始的时间
startnow = now + datetime.timedelta(days=3)
# 六十天后的时间
endnow = startnow + datetime.timedelta(days=60)
# 六十天后的时间转换成字符串
startnow = str(startnow.strftime('%Y-%m-%d'))    
endnow = str(endnow.strftime('%Y-%m-%d'))
 
def func(dname,aname):
    global startnow #用全局变量把当天日期导进来
    # now 是当天的日期，一般抓取都是从当天开始抓这
    urls = 'https://www.ly.com/flights/itinerary/oneway/'+ str(dname) +'-'+ str(aname) + '?date='+startnow+'&fromairport=&toairport=&from=%E4%B8%8A%E6%B5%B7&to=%E5%8C%97%E4%BA%AC&childticket=0,0'
    global endnow #用全局变量把60天后的日期导进来
    
    f = open('同城旅游.csv','a+',encoding='utf-8',newline='')
    csv_writer = csv.writer(f)
                
    driver=Options()#webdriver.Options()
    driver.add_experimental_option('useAutomationExtension', False)
    driver.add_experimental_option("excludeSwitches", ['enable-automation'])
    prefs = {"profile.managed_default_content_settings.images": 2} # 不加载图片
    driver.add_experimental_option("prefs",prefs)
    driver=webdriver.Chrome(options=driver)
    driver.get(urls)
    while True:
        # 加载完的界面 ,提取整个页面完整的数据源码
        html = driver.page_source
        response = etree.HTML(html)
        #print(u'全部加载完成')
        
        # 通过xpath把加载完的页面数据全部取出来，做一一对应
        for each in response.xpath("//div[@class='dataListContainer']"):
            time.sleep(8)

            flight_id = each.xpath(".//p[@class='flight-item-name']/text()")
            starttime = each.xpath(".//div[@class='f-startTime f-times-con']/strong/text()")
            endtime = each.xpath(".//div[@class='f-endTime f-times-con']/strong/text()")
            #endtime = re.sub(r'\s+','', endtime)
            print(flight_id)
            print(starttime)
            print(endtime)
            dcity = response.xpath("//*[@id='__layout']/div/section/div/div[4]/div[2]/div[1]/strong/text()[1]/text()")
            acity = response.xpath("//*[@id='__layout']/div/section/div/div[4]/div[2]/div[1]/strong/text()[2]/text()")
            print(dcity)
            print(acity)
            dates = response.xpath("//*[@id='__layout']/div/section/div/div[4]/div[2]/div[1]/span/text()")# 出发日期
            print(dates)
            official_price = each.xpath(".//div[@class='head-prices']/strong/em/text()")# 价格
            print(official_price)
      
 
if __name__ == "__main__":
    
    #f = open('同程旅游.csv','a+',encoding='utf-8',newline='')
    #csv_writer = csv.writer(f)
    #csv_writer.writerow(["departurename" ,"arrivename","flightNo","flightDate","start","end","price"])#构建列表头
    #f.close()
    for j in dlist:
        for i in alist:
            func(j,i)
    print("done")




