import requests
from bs4 import BeautifulSoup
import urllib.request
import json
import csv
import time

headers = {
     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like 09	Gecko) Chrome/55.0.2883.87 Safari/537.36'
 }
url_1s = []
url_2s = []
infos = []

def get_url():
    for i in range(1,199,2):
        j = i*50
        u = 'https://search.jd.com/Search?keyword=%E7%AC%94%E8%AE%B0%E6%9C%AC%E7%94%B5%E8%84%91&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&ev=exprice_3500-4500%5E&page=' + str(i) + '&s=' + str(j) + '&click=0'
        url_1s.append(u)
    for url in url_1s:
        r = requests.get(url,headers=headers)
        r.encoding=r.apparent_encoding
        soup = BeautifulSoup(r.text,'html.parser')# html.parser
        url = (soup.find_all(class_="p-img"))
        for u in url:
            u = u.find('a').get('href')
            url_2s.append('https:'+u)


def get_info(url):
    r = requests.get(url, headers=headers)
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, 'html.parser')  # html.parser
    info = soup.find_all(class_="sku-name")
    sku = url.split('/')[-1].strip(".html")
    price_url = "https://p.3.cn/prices/mgets?skuIds=J_" + sku
    response = urllib.request.urlopen(price_url)
    content = response.read()
    result = json.loads(content)
    inf = info[0].get_text().strip()
    price= result[0]['p']
    data = {
        inf,
        price
    }
    infos.append(data)
    with open('jd.csv', 'a', encoding='utf-8') as f:
        f_csv = csv.writer(f, )
        f_csv.writerows(infos)
        f.close()

if __name__ == "__main__":
    get_url()
    i =1
    for url in url_2s:
       get_info(url)
       i=i+1
       if i%50==0:
           print('finish'+str(i))
           time.sleep(1)