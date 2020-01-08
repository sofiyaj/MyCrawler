from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from pprint import pprint


## 浏览器配置
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless') #隐藏浏览器界面
chrome_options.add_argument('--disable-gpu')

## 驱动配置
browser = webdriver.Chrome(chrome_options=chrome_options)
wait=WebDriverWait(browser,10)

##定义方法

def toIframe1(): #进入iframe
    browser.switch_to.default_content()
    iframe1 = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,'#contentmain')))
    browser.switch_to.frame(iframe1)

def toIframe2(): #进入iframe内的iframe
    browser.switch_to.default_content()
    iframe1 = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,'#contentmain')))
    browser.switch_to.frame(iframe1)
    iframe2 = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,'#home_main')))
    browser.switch_to.frame(iframe2)

def toIframe3(): #进入iframe内的iframe
    browser.switch_to.default_content()
    iframe1 = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,'#contentmain')))
    browser.switch_to.frame(iframe1)
    iframe3 = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,'#resource_main')))
    browser.switch_to.frame(iframe3)


class obj: #obj对象
    def __init__(self): #对象属性
        self.state = ''
        self.code = ''
        self.information = ''
        self.url = ''
    def print(self): #对象方法
        pprint(self.__dict__)

def getContent(): # 获取内容
    toIframe2()
    try:
        lis = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,'body > div > div.box > ul > li')))
    except:
        TimeoutError
    for li in lis:
        f = open('a.txt','a')
        toIframe2()
        item = obj()
        item.state = li.find_element_by_tag_name('h2').text
        if item.state.find('成交')!=-1:
            item.code = li.find_element_by_css_selector('h3 > em').text
            item.url = li.find_element_by_css_selector('span.boxtxt2 > input').get_attribute('onclick')
            browser.execute_script(item.url)
            toIframe3()
            item.information = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#contain > div.cotain-box > table > tbody > tr:nth-child(2) > td.td_line1 > table > tbody > tr:nth-child(2)'))).get_attribute('outerHTML')
            #item.print()
            f.write(str(item.__dict__))
            f.write('\n')
            browser.execute_script('javascript:goReturn();')
        f.close()
    

   
##main

browser.get("http://land.zjgtjy.cn/GTJY_ZJ/go_home") #模拟访问

try:
    btnZJ = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#site-nav > ul > li:nth-child(1) > div > a')))
except:
    TimeoutError
btnZJ.click()
browser.execute_script('javascript:resoult();')
browser.execute_script('javascript:window.hide1();')
browser.execute_script('javascript:window.hide2();')

for i in range(1,10+1): #每次爬10页
    print(i) #后台输出当前页数
    f = open('a.txt','a')
    f.write(str(i))
    f.write('\n')
    f.close()
    getContent()
    toIframe1()
    try:
        btnNext = wait.until(EC.element_to_be_clickable((By.LINK_TEXT,'下一页')))
    except:
        TimeoutError
    btnNext.click()
    time.sleep(2)


print('完成')
browser.quit()