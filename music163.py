#coding:utf-8
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import csv


'''
作者：pk哥
公众号：Python知识圈
日期：2018/07/21
代码解析详见公众号「Python知识圈」。

'''

browser = webdriver.Chrome()
wait = WebDriverWait(browser,5)    #设置等待时间


#返回歌手名字和歌手id
def get_singer(url):
    browser.get(url)
    browser.switch_to.frame('g_iframe')
    html = browser.page_source
    soup=BeautifulSoup(html,'lxml')
    info=soup.select('.nm.nm-icn.f-thide.s-fc0')  #有图歌手m-artist-box > li:nth-child(1) > p > a.nm.nm-icn.f-thide.s-fc0 #无图歌手#m-artist-box > li:nth-child(91) > a
    sname=[]
    songids=[]
    for snames in info:
        name=snames.get_text()
        songid=str(re.findall('href="(.*?)"',str(snames))).split('=')[1].split('\'')[0]
        sname.append(name)
        songids.append(songid)
    return sname,songids


def song_url():
    sname, songids = get_singer(url)
    top50urls=[]
    for id in songids:
        top50url = 'http://music.163.com/#/artist?id={}'.format(id)  #拼接热门歌曲 top 50 的url
        top50urls.append(top50url)
    return top50urls


def song_name():
    songnames=[]
    for top50url in song_url():
        browser.get(top50url)
        browser.switch_to.frame('g_iframe')
        html = browser.page_source
        soup = BeautifulSoup(html, 'lxml')
        songinfo = soup.select('div div div span a b')
        songname=re.findall('title="(.*?)"',str(songinfo))
        songnames.append(songname)
    return songnames


def get_data():
    sname, songids=get_singer(url)
    songnames=song_name()
    data=[]
    for snames,songs in zip(sname,songnames):
        info = {}
        info['歌手名字']=snames
        info['top50歌曲'] =songs
        #将字典里 value 值为list转换为一对一关系
        for i in info:
            for j in info[i]:
                info2={i:j}
                data.append(info2)
    return data


def download2csv():
    print('保存歌手信息中...请稍后查看')
    with open('E:\\歌手top50.csv','w',newline='',encoding='utf-8') as f:
        fieldnames = ['歌手名字', 'top50歌曲']
        writer=csv.DictWriter(f,fieldnames=fieldnames)
        writer.writeheader()
        data=get_data()
        writer.writerows(data)
        print('保存成功')


idlist=[1001,1002,1003,2001,2002,2003,4001,4002,4003,6001,6002,6003,7001,7002,7003]
#1开头：华语；2开头：欧美，4：其他；6：日本；7：韩国
id=1001
url='http://music.163.com/#/discover/artist/cat?id={}&initial=-1'.format(str(id))
download2csv()
