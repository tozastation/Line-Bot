import json
import requests
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
"""
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
