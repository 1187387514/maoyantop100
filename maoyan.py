import re
import requests
import json
import time
from multiprocessing import Pool

#此代码用于爬取猫眼电影上排行前100的信息
#获取html信息
def gethtml(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("获取网页失败")

#解析html信息
def parsehtml(html):
    r = re.compile('<i class="board-index.*?>(.*?)</i>.*?<div.*?movie-item-info.*? href="(.*?)".*?title="(.*?)".*?"star">(.*?)</p>.*?releasetime">(.*?)</p>',re.S)
    items = re.findall(r,html)
    for item in items:
        xuhao = item[0]
        href = item[1]
        title = item[2]
        star = item[3].strip()[3:]
        time = item[4].strip()[5:]
        yield {'index':xuhao,
               'href':href,
               'title':title,
               'star':star,
               'time':time}
#把获取的html信息存放到一个txt文件里
def writefile(item):
    with open('maoyan.txt','a',encoding = 'utf-8') as f:
        f.write(str(item)+"\n")


def main(i):
    url = 'https://maoyan.com/board/4'+'?offset={}'.format(i*10)
    html = gethtml(url)
    items = parsehtml(html)
    for item in items:
        writefile(item)

if __name__ == '__main__':
    for i in range(10):
        main(i)
