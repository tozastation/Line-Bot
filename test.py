import json
import requests
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
sentence1 = "おはよううさ。今日の天気うさ。\n"
sentence2 = 'City :'+str(city)+'\n'
sentence3 = 'temp :'+str(temp)+'\n'
sentence4 = 'weather :'+str(weather)+'\n'
sentence = sentence1+sentence2+sentence3+sentence4
print(sentence)
