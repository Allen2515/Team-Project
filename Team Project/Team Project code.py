from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import datetime
import pandas as pd

# 設定瀏覽器選項
options = Options()
# 建立 driver
s = Service(r"chromedriver.exe")
chrome = webdriver.Chrome(service=s, options=options)

year = datetime.datetime.now().year
month = datetime.datetime.now().month
day = datetime.datetime.now().day
hour = datetime.datetime.now().hour

# 新聞查詢
search = ['中央大學', '周景揚']
newsweb = ['https://news.google.com.tw/', 'https://www.cna.com.tw/', 'https://udn.com/', 'https://search.ltn.com.tw/', 'https://tol.chinatimes.com/CT_NS/ctsearch.aspx']

all = []
check = []

def googlenews(url):
    chrome.get(url)
    content = chrome.find_element(By.CLASS_NAME, 'Ax4B8')
    for item in search:
        content.send_keys('\"' + item + '\" when:1d')
        content.send_keys(Keys.ENTER)
        chrome.get(chrome.current_url)
        intourl = chrome.find_elements(By.CLASS_NAME, 'WwrzSb')
        tempdate = chrome.find_elements(By.CLASS_NAME, 'hvbAAd')
        for i in range (len(intourl)):
            if int(tempdate[i].get_attribute('datetime')[8:10]) != day:
                continue
            newsurl = intourl[i].get_attribute('href')
            newchrome = webdriver.Chrome(service=s, options=options)
            newchrome.get(newsurl)
            time.sleep(3)
            newstitle = newchrome.title
            newchrome.close()
            tempdict = {'新聞標題':newstitle, '新聞網址':newsurl}
            if (not(newstitle in check)):
                all.append(tempdict)
                check.append(newstitle)
        chrome.get(url)
        content = chrome.find_element(By.CLASS_NAME, 'Ax4B8')
        time.sleep(0.1)

def cnanews(url):
    chrome.get(url)
    for item in search:
        tempurl = chrome.current_url + 'search/hysearchws.aspx?q=' + item
        chrome.get(tempurl)
        intourl = chrome.find_elements(By.CSS_SELECTOR, '.mainList [href]')
        tempdate = chrome.find_elements(By.CLASS_NAME, 'date')
        for i in range (len(intourl)):
            if tempdate[i].text[:4] < str(year) or tempdate[i].text[5:7] < str(month) or tempdate[i].text[8:10] < str(day):
                break
            newsurl = intourl[i].get_attribute('href')
            newchrome = webdriver.Chrome(service=s, options=options)
            newchrome.get(newsurl)
            time.sleep(1)
            newstitle = newchrome.title
            newchrome.close()
            tempdict = {'新聞標題':newstitle, '新聞網址':newsurl}
            if (not(newstitle in check)):
                all.append(tempdict)
                check.append(newstitle)
        chrome.get(url)
        time.sleep(0.1)

def udnnews(url):
    chrome.get(url)
    for item in search:
        tempurl = newsweb[2] + 'search/word/2/' + item
        chrome.get(tempurl)
        intourl = chrome.find_elements(By.CLASS_NAME, 'story-list__text')
        tempdate = chrome.find_elements(By.CLASS_NAME, 'story-list__time')
        for i in range (len(intourl)):
            if tempdate[i].text[:4] < str(year) or tempdate[i].text[5:7] < str(month) or tempdate[i].text[8:10] < str(day):
                break
            newsurl = intourl[i].find_element(By.TAG_NAME, 'a').get_attribute('href')
            newchrome = webdriver.Chrome(service=s, options=options)
            newchrome.get(newsurl)
            time.sleep(1)
            newstitle = newchrome.title
            newchrome.close()
            tempdict = {'新聞標題':newstitle, '新聞網址':newsurl}
            if (not(newstitle in check)):
                all.append(tempdict)
                check.append(newstitle)
        chrome.get(url)
        time.sleep(0.1)

def ltnnews(url):
    chrome.get(url)
    content = chrome.find_element(By.ID, 'keyword_search')
    for item in search:
        content.send_keys(item)
        content.send_keys(Keys.ENTER)
        chrome.get(chrome.current_url)
        intourl = chrome.find_elements(By.CLASS_NAME, 'cont')
        for i in range (len(intourl)):
            newsurl = intourl[i].get_attribute('href')
            newchrome = webdriver.Chrome(service=s, options=options)
            newchrome.get(newsurl)
            time.sleep(1)
            newstitle = newchrome.title
            tempdate = newchrome.find_element(By.CLASS_NAME, 'time')
            if tempdate.text[:4] < str(year) or tempdate.text[5:7] < str(month) or tempdate.text[8:10] < str(day):
                newchrome.close()
                break
            newchrome.close()
            tempdict = {'新聞標題':newstitle, '新聞網址':newsurl}
            if (not(newstitle in check)):
                all.append(tempdict)
                check.append(newstitle)
        chrome.get(url)
        content = chrome.find_element(By.ID, 'keyword_search')
        time.sleep(0.1)
        
# def chinanews(url):
#     chrome.get(url)
#     for item in search:
#         tempurl = chrome.current_url + 'search/hysearchws.aspx?q=' + item
#         chrome.get(tempurl)
#         intourl = chrome.find_elements(By.CSS_SELECTOR, '.mainList [href]')
#         tempdate = chrome.find_elements(By.CLASS_NAME, 'date')
#         for i in range (len(intourl)):
#             if tempdate[i].text[:4] < str(year) or tempdate[i].text[5:7] < str(month) or tempdate[i].text[8:10] < str(day):
#                 break
#             newsurl = intourl[i].get_attribute('href')
#             newchrome = webdriver.Chrome(service=s, options=options)
#             newchrome.get(newsurl)
#             time.sleep(1)
#             newstitle = newchrome.title
#             newchrome.close()
#             tempdict = {'新聞標題':newstitle, '新聞網址':newsurl}
#             if (not(newstitle in check)):
#                 all.append(tempdict)
#                 check.append(newstitle)
#         chrome.get(url)
#         time.sleep(0.1)

for news in range (len(newsweb)):
    url = newsweb[news]
    if news == 0:
        googlenews(url)
    if news == 1:
        cnanews(url)
    if news == 2:
        udnnews(url)
    if news == 3:
        ltnnews(url)
    # if news == 4:
    #     chinanews(url)
    
df = pd.DataFrame(all)
df.to_excel('news.xlsx')

# 等待 5 秒鐘以載入頁面
time.sleep(5)
# 關閉瀏覽器視窗
# chrome.close()