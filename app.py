from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait



chrome_options = webdriver.ChromeOptions()

chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

browser = webdriver.Chrome(chrome_options=chrome_options)
mainUrl = "http://land.zjgtjy.cn/GTJY_ZJ/go_home"
browser.get(mainUrl)

siteNav = browser.find_element(By.ID,'site-nav')
btnZJ = siteNav.find_element(By.XPATH,'.//ul/li[1]/div/a')
btnZJ.click()

browser.execute_script('javascript:resoult();')

iframe1 = browser.find_element_by_id('contentmain')
browser.switch_to.frame(iframe1)
iframe2 = browser.find_element_by_id('home_main')
browser.switch_to.frame(iframe2)

li = browser.find_elements_by_css_selector('div.box > ul > li')

browser.quit()