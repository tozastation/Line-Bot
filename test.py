import json
import requests
import re
from datetime import datetime as dt
"""
API_KEY = "b658161bac2942afc45703a43ff1b362"
api = "http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={key}"
city_name = 'Hakodate'
url = api.format(city = city_name, key = API_KEY)
print(url)
response = requests.get(url)
data = json.loads(response.text)
K = 273.15
city = data['name']
temp = round(data['main']['temp']-K,2)
weather = data["weather"][0]["main"]
description = data["weather"][0]["description"]
line1 = "おはよううさ〜。今日の天気うさ。\n"
line2 = 'City :'+str(city)+'\n'
line3 = 'temp :'+str(temp)+'\n'
line4 = 'weather :'+str(weather)+'\n'
line5 = 'description : '+str(description)
sentence = line1+line2+line3+line4+line5
print(sentence)
print(data)
sentence = '@tozasan'
if '@' in sentence:
    print(sentence.replace('@', ''))
import urllib
from xml.etree import ElementTree
import xml.dom.minidom as md
url = 'http://news.nicovideo.jp/categories/10?rss=2.0'
response = urllib.request.urlopen(url)
root = ElementTree.fromstring(response.read())
document = md.parseString(ElementTree.tostring(root, 'utf-8'))
links = []
for a in document.getElementsByTagName('link'):
    links.append(a.toxml().rstrip('</link>').lstrip('</link>'))
del links[0]
links.insert(0, 'この時間のニュースうさ')
for link in links:
    print(link)

titles = []

for a in document.getElementsByTagName('title'):
    titles.append(a.toxml().rstrip('</title>').lstrip('</title>'))

del titles[0]
titles.insert(0, '')
for title in titles:
    print(title)
"""
# coding: UTF-8
import urllib.request
from bs4 import BeautifulSoup

# アクセスするURL
# url = "http://www.hakobus.jp/result.php?in=165&out=3"
url = "http://www.hakobus.jp/result.php?in=165&out=156"
# url = "https://student.fun.ac.jp/up/faces/up/po/pPoa0202A.jsp?fieldId=form1:Poa00201A:htmlParentTable:1:htmlDetailTbl:1:linkEx1"
# URLにアクセスする htmlが帰ってくる → <html><head><title>経済、株価、ビジネス、政治のニュース:日経電子版</title></head><body....
html = urllib.request.urlopen(url)

# htmlをBeautifulSoupで扱う
soup = BeautifulSoup(html, "html.parser")
bus_late = soup('td', width='160')  # 遅延情報
bus_type = soup('td', width='140')  # 系統
bus_end = soup('td', width='120')   # 終点
bus_time = soup('div', align='center')  # バス時刻


for a in bus_late:
    late = str(a)
    late = late.replace('<td width="160">', '')
    late = late.replace('</td>', '')
    if late is '':
        print('無し')
    elif late in '*****':
        print('未定')
    else:
        print(late)

for a in bus_type:
    t = str(a)
    t = t.replace('<td width="140">', '')
    t = t.replace('</td>', '')
    t = t.replace('<div align="center">', '')
    t = t.replace('<br/>', '')
    t = t.replace('\n', '')
    s = t.split(' ')
    t = s[0].replace('<!--', '')
    print(t)


for a in bus_end:
    end = str(a)
    end = end.replace('<td width="120">', '')
    end = end.replace('</td>', '')
    end = end.replace('<div align="center">', '')
    end = end.replace('</div>', '')
    print(end)


for a in bus_time:
    time = str(a)
    time = time.replace('<td width="160">', '')
    time = time.replace('</td>', '')
    time = time.replace('<div align="center">', '')
    time = time.replace('</div>', '')
    time = time.replace('\n', '')
    try:
        time = dt.strptime(time, '%H:%M')
        hour = str(time.hour)
        minute = str(time.minute)
        print(hour+':'+minute)
    except Exception as e:
        pass
