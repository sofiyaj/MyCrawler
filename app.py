from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import time,requests,json


## 浏览器配置
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless') #隐藏浏览器界面
chrome_options.add_argument('--disable-gpu')

## 驱动配置
browser = webdriver.Chrome(chrome_options=chrome_options)
wait=WebDriverWait(browser,10)

f=open('last.id','r')
rlastid = f.readline()
f.close()
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

def Update2Confluence(time,landid,content):
    jsondata = {
        "type":"page",
        "title": time+"-"+landid,
        "ancestors":[{"id":7602339}], 
        "space":{"key":"LTI"},
        "body":{
            "storage":{
                "value":"<ac:structured-macro ac:name=\"html\"><ac:plain-text-body><![CDATA[\
                            "+content+"\
                        ]]></ac:plain-text-body></ac:structured-macro>",
                "representation":"storage"
                }
            }
        }
    r = requests.post('http://file.znmq.net/rest/api/content/',
            data=json.dumps(jsondata),
            auth=('robot','sHfR6m1nH_'),
            headers=({'Content-Type':'application/json;charset=utf-8'})
        )
    return r

class obj: #obj对象
    def __init__(self): #对象属性
        self.state = ''
        self.landid = ''
        self.information = ''
        self.url = ''
    def print(self): #对象方法
        print(self.__dict__)

def getContent(): # 获取内容
    toIframe2()
    try:
        lis = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,'body > div > div.box > ul > li')))
    except:
        TimeoutError
        browser.quit()
    for li in lis:
        f = open('a.txt','a')
        toIframe2()
        item = obj()
        item.state = li.find_element_by_tag_name('h2').text
        item.landid = li.find_element_by_css_selector('h3 > em').text
        item.transactionTime = li.find_element_by_css_selector('span.boxtxt1 > em:nth-child(11)').text
        if item.landid != rlastid:
            if item.state.find('成交')!=-1 and item.state.find('未成交')==-1:
                item.url = li.find_element_by_css_selector('span.boxtxt2 > input').get_attribute('onclick')
                browser.execute_script(item.url)
                time.sleep(0.3)
                toIframe3()
                item.information = wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="contain"]/div[3]/table/tbody/tr[2]/td[2]/table/tbody/tr[2]/td/table'))).get_attribute('outerHTML').replace('\t','').replace('\n','')
                print(Update2Confluence(item.transactionTime,item.landid,item.information))
                #item.print()
                f.write(str(item.__dict__))
                f.write('\n')
                browser.execute_script('javascript:goReturn();')
            f.close()
            time.sleep(0.1)
        else:
            return False
    

   
##main

browser.get("http://land.zjgtjy.cn/GTJY_ZJ/go_home") #模拟访问

try:
    btnZJ = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#site-nav > ul > li:nth-child(1) > div > a')))
except:
    TimeoutError
    browser.quit()
btnZJ.click()
browser.execute_script('javascript:resoult();')
browser.execute_script('javascript:window.hide1();')
browser.execute_script('javascript:window.hide2();')

toIframe2()
f=open('last.id','w')
wlastid = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,('body > div > div.box > ul > li:nth-child(1) > h3 > em')))).text
f.write(wlastid)
f.close
for i in range(1,20+1): #最多爬20页
    print('第'+str(i)+'页') #后台输出当前页数
    f = open('a.txt','a')
    flag=getContent()
    if flag==False:
        break
    toIframe1()
    try:
        btnNext = wait.until(EC.element_to_be_clickable((By.LINK_TEXT,'下一页')))
    except:
        TimeoutError
        browser.quit()
    btnNext.click()
    time.sleep(0.5)


print('爬取完成')
browser.quit()