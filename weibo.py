# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import time
import csv

headers = {
     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like 09	Gecko) Chrome/55.0.2883.87 Safari/537.36',
     'Cookie': ''}

urls_1 = []
infss = []
infs_1 =[]
infs_2 =[]
def get_url():
    res = requests.get('https://s.weibo.com/top/summary?cate=realtimehot',headers=headers)
    soup = BeautifulSoup(res.text,'html.parser')
    infs = soup.select('#pl_top_realtimehot > table > tbody > tr > td > a')
    ranks = soup.select('#pl_top_realtimehot > table > tbody > tr > td.ranktop')
    links = soup.select('#pl_top_realtimehot > table > tbody > tr > td > a')
    amounts = soup.select('#pl_top_realtimehot > table > tbody > tr > td > span')
    for inf, rank, link,amount in zip(infs,ranks,links,amounts):
            data = {
                'inf':inf.get_text(),
                'rank':rank.get_text(),
                'amount': amount.get_text(),
                'link':'https://s.weibo.com'+link.get("href")
            }
            urls_1.append(data)



def getinf(url):
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    headd = soup.select('#pl_feedtop_top > div.searchbox > div > input[type=text]')
    infs = soup.find_all(class_ = 'txt')
    for inf in infs:
        xx=u'([\u4e00-\u9fa5]+)'
        inf = re.findall(xx,str(inf))
        infs_1.append(inf)
    times = soup.find_all(class_ = 'from')
    for time in times:
        time = time.text
        infs_2.append(time.strip())
    q = 1
    for a, b in zip(infs_1, infs_2):
        data = [headd[0].get('value'),a,b]
        with open('weibo.csv', 'a+', encoding='utf-8') as f:
            f_csv = csv.writer(f, )
            f_csv.writerow(data)
            f.close()
        if (q>=100) and (q%100==0):
            print("本页已完成"+str(q)+"条数据")
        q=q+1

if __name__ == "__main__":
    get_url()
    for url in urls_1:
        for i in range(1, 40):
            url_1 = url['link'] + 'page=' +str(i)
            print(url_1)
            if 'void(0)' in url:
                pass
            else:
                try:
                    getinf(url)
                    time.sleep(3)
                    print('已完成' + str(i) + '页数据')
                except IndexError:
                    print('出了一个问题')
                    pass
                continue

    with open('stop.csv', 'a+', encoding='utf-8') as f:
        f_csv = csv.writer(f, )
        f_csv.writerow('over')
        f.close()
