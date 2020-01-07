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
# chrome_options.add_argument('--headless') #隐藏浏览器界面
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


class obj: #obj对象
    def __init__(self): #对象属性
        self.state = ''
        self.code = ''
        self.name = ''
        self.position = ''
        self.useFor = ''
        self.endTime = ''
        self.finalPrice = ''
    def print(self): #对象方法
        pprint(self.__dict__)

def write(item):
    if item.state.find('成交')!=-1:
        f.write(str(item.__dict__))
        f.write('\n')

def getContent(): # 获取内容
    toIframe2()
    lis = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,'body > div > div.box > ul > li')))
    items=[]
    for li in lis:
        item = obj()
        item.state = li.find_element_by_tag_name('h2').text
        item.code = li.find_element_by_tag_name('h3').text
        item.name = li.find_element_by_css_selector('span.boxtxt1 > span:nth-child(1) > em').text
        item.position = li.find_element_by_css_selector('span.boxtxt1 > span:nth-child(3) > em').text
        # item.useFor = li.find_element_by_css_selector('span.boxtxt1 > em:nth-child(5)').text
        # item.endTime = li.find_element_by_css_selector('span.boxtxt1 > em:nth-child(9)').text
        # item.finalPrice = li.find_element_by_css_selector('span.boxtxt1 > em:nth-child(15)').text
        # item.print()
        write(item)

   
##main

browser.get("http://land.zjgtjy.cn/GTJY_ZJ/go_home") #模拟访问

try:
    btnZJ = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#site-nav > ul > li:nth-child(1) > div > a')))
    btnZJ.click()
    browser.execute_script('javascript:resoult();')
except:
    TimeoutError

items=[]
f = open('a.txt','w')
for i in range(2,10+1): #每次爬10页
    try:
        toIframe1()
        btnNext = wait.until(EC.element_to_be_clickable((By.LINK_TEXT,'下一页')))
        btnNext.click()
        time.sleep(0.5)
        print(i) #后台输出当前页数
        getContent()
        time.sleep(0.5)
    except:
        TimeoutError

f.close()
print('完成')
browser.quit()