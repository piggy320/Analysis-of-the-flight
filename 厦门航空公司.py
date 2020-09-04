
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
# 机场代码列表
dlist= ["XMN"]
alist= ["TSN", "SHA", "HGH"]#, "WUH","CTU","HGH","WUH"]#"DLC": "大连","SHA": "上海", "CAN": "广州","TSN": "天津"
                                                    #"CTU": "成都","HGH": "杭州", "WUH": "武汉","SIA": "西安","CKG": "重庆",

# 现在的时间
now = datetime.datetime.now()
# 递增的时间
delta = datetime.timedelta(days=1)
# 三十天后的时间
endnow = now + datetime.timedelta(days=6)
# 三十天后的时间转换成字符串
endnow = str(endnow.strftime('%Y-%m-%d'))
now = str(now.strftime('%Y-%m-%d'))
 
def func(aname):
    dname='XMN'
    #传进来的参数是"FOC"这样，所以完整的url需要拼接
    global now #用全局变量把当天日期导进来
    # now 是当天的日期，一般抓取都是从当天开始抓这
    #urls = 'https://et.xiamenair.com/xiamenair/book/findFlights.action?lang=zh&tripType=0&queryFlightInfo=' + str(url) + ','+str(now)                              
    urls = 'https://www.xiamenair.com/zh-cn/nticket.html?tripType=OW&orgCodeArr%5B0%5D=' + str(dname) + '&dstCodeArr%5B0%5D=' + str(aname) + '&orgDateArr%5B0%5D='+now+'&dstDate=&isInter=false&adtNum=1&chdNum=0&JFCabinFirst=false&acntCd=&mode=Money&partner=false&jcgm=false'
    global endnow #用全局变量把6天后的日期导进来
 
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
        print(u'全部加载完成')
        
        # 通过xpath把加载完的页面数据全部取出来，做一一对应
        i=0
        for each in response.xpath("//div[@class='left']"):
            time.sleep(5)
            if(i==0):#第一条为空
                i=1
                continue
            print('ok')
            hangci = each.xpath(".//span[@class='flight-num']/text()")
            starttime = each.xpath(".//div[@class='start']/div[@class='time']/text()")
            endtime = each.xpath(".//div[@class='end']/div[@class='time']/text()")#("normalize-space(.//div[@class='end']/div[@class='time']/text())")
            #endtime = re.sub(r'\s+','', endtime)
            print(hangci)
            print(starttime)
            print(endtime)
            citys = response.xpath("/html/body/div/div[4]/div[2]/div/div/div[1]/div[2]/div/div[1]/span[1]/div/text()")[0]
            print(citys)
            flightDate = response.xpath("/html/body/div/div[4]/div[2]/div/div/div[1]/div[1]/ul/li[4]/p[1]/text()")[0]#("/html/body/div/div[4]/div[2]/div/div/div[1]/div[2]/div/div[1]/span[2]/text()")[0]  # 出发日期
            print(flightDate)
            official_price = each.xpath(".//div[@class='flight-info clearfix']/div[@class='price']//strong/text()")  # 价格
            print(official_price)

        #driver.quit()
        #break
        #'''
        # 定位下一日期
        date = response.xpath("/html/body/div/div[4]/div[2]/div/div/div[1]/div[1]/ul/li[5]/p[1]/text()")
         
        # 当下一日期等于指定日期，就停止循环
        if (str(date) == endnow):
            #time.sleep(5)
            driver.quit()
            break
        else:
            # 一直点击下一页
            qq = driver.find_element_by_xpath("/html/body/div/div[4]/div[2]/div/div/div[1]/div[1]/ul/li[5]")
            ActionChains(driver).click(qq).perform()
            time.sleep(5)
        #'''
 
 
 
if __name__ == "__main__":

    for i in alist:
        func(i)
    
    print("done")