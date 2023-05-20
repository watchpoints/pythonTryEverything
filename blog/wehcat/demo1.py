# https://zhuanlan.zhihu.com/p/372340559
#导入所需模块
from selenium import webdriver

from bs4 import BeautifulSoup

import time

from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.common.keys import Keys

import csv

import requests

url = '微信公众平台'

#输入驱动位置

driver = webdriver.Chrome('/storage/jupyter/shenr/微信公众号爬虫/chromedriver.exe')

#打开网址

driver.get(url)

#最大化浏览器窗口，更好的内容定位

driver.maximize_window()

time.sleep(10)

##点击图文消息

driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[3]/div[2]/div/div[1]/div/div').click()

time.sleep(3)

#跳转到新界面

driver.switch_to.window(driver.window_handles[1])

time.sleep(3)

#点击超链接

driver.find_element_by_xpath('//*[@id="js_editor_insertlink"]').click()

time.sleep(2)

#点击选择其他公众号

driver.find_element_by_xpath('//*[@id="vue_app"]/div[2]/div[1]/div/div[2]/div[2]/form[1]/div[3]/div/div/p/div/button').click()

#输入杭州本地宝，进行搜索（如爬取别的公众号，对应修改即可）

driver.find_element_by_xpath('//*[@id="vue_app"]/div[2]/div[1]/div/div[2]/div[2]/form[1]/div[3]/div/div/div/div/span/input').send_keys('杭州本地宝')

time.sleep(5)

#选择杭州本地宝公众号

driver.find_element_by_xpath('//*[@id="vue_app"]/div[2]/div[1]/div/div[2]/div[2]/form[1]/div[3]/div/div/div/div[2]/ul/li[1]/div[1]').click()


###提取当前页中文章的发布时间以及文章地址

def get_url(num):

content = []

#输入想要爬取的页数

driver.find_element_by_xpath('//*[@id="vue_app"]/div[2]/div[1]/div/div[2]/div[2]/form[1]/div[4]/div/div/div[3]/span[2]/input').send_keys('num')

#点击跳转

driver.find_element_by_xpath('//*[@id="vue_app"]/div[2]/div[1]/div/div[2]/div[2]/form[1]/div[4]/div/div/div[3]/span[2]/a').click()

soup = BeautifulSoup(driver.page_source,'lxml')

all_label_tag = soup.findAll('label',attrs={'class':'inner_link_article_item'})

for label in all_label_tag:

try:

time = label.find('div',attrs={'class':'inner_link_article_date'}).text

url = label.find('a')['href']

content.append([time,url])

except:

print('出错啦')

return content

#杭州本地宝的所有文章总共有102页，所以每一页都需要进行提取，并将其存储在列表中

all_content = []

for i in range(102):

all_content.append(get_url(i))

#去除大列表中的小列表

all_content = sum(all_content,[])


#提取所有网址的文章内容、发布时间、来源以及标题

def get_content(all_list):

with open('杭州本地宝文章.csv','w',encoding='utf-8-sig',newline='') as file:

writer = csv.writer(file)

writer.writerow(['时间','来源','标题','内容'])

for url in all_list:

try:

#对网址发送请求

response = requests.get(url[1])

#解析成lxml

soup = BeautifulSoup(response.content.decode('utf-8'),'lxml')

#提取文章来源

origin = soup.find('span',attrs={'class':'rich_media_meta rich_media_meta_nickname'}).a.text.replace('\n','').replace(' ','')

time = url[0]

#提取文章标题

title = soup.find('h2',attrs={'class','rich_media_title'}).text.replace(' ','').replace('\n','')

#提取文章内容

content = soup.find('section',attrs={'data-role':'outer'}).text

writer.writerow([time,origin,title,content])

except:

response = requests.get(url[1])

time = url[0]

soup = BeautifulSoup(response.content.decode('utf-8'),'lxml')

origin = soup.find('span',attrs={'class':'rich_media_meta rich_media_meta_nickname'}).a.text.replace('\n','').replace(' ','')

title = soup.find('h2',attrs={'class','rich_media_title'}).text.replace(' ','').replace('\n','')

content = soup.find('div',attrs={'class':'rich_media_content'}).text.replace('\n','')

writer.writerow([time,origin,title,content])

get_content(all_content)