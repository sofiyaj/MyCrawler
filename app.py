from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import re
import time


# 浏览器配置
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

# 驱动配置
browser = webdriver.Chrome(chrome_options=chrome_options)
wait=WebDriverWait(browser,10)

#模拟访问
mainUrl = "http://land.zjgtjy.cn/GTJY_ZJ/go_home"
browser.get(mainUrl)

try:
    btnZJ = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#site-nav > ul > li:nth-child(1) > div > a')))
    btnZJ.click()
    browser.execute_script('javascript:resoult();')
except:
    TimeoutError

def toIframe1():
    browser.switch_to.default_content()
    iframe1 = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,'#contentmain')))
    browser.switch_to.frame(iframe1)

def toIframe2():
    browser.switch_to.default_content()
    iframe1 = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,'#contentmain')))
    browser.switch_to.frame(iframe1)
    iframe2 = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,'#home_main')))
    browser.switch_to.frame(iframe2)

def getContent():
    toIframe2()
    lis = wait.until(EC.presence_of_elements_located(By.CSS_SELECTOR,'body > div > div.box > ul > li'))
    print('\n'.join([ls.find_element_by_tag_name('h3').text for ls in lis]))



for i in range(2,10+1):
    try:
        toIframe1()
        btnNext = wait.until(EC.element_to_be_clickable((By.LINK_TEXT,'下一页')))
        btnNext.click()
        print(i)
        # getContent()
        time.sleep(1)
        
    except:
        TimeoutError


# print('\n'.join([ls.find_element_by_tag_name('a').text for ls in lis]))
time.sleep(2)
browser.quit()