import json
import requests


class Info(object):
    def __init__(self):
        self.__YOUR_CHANNEL_ACCESS_TOKEN = 'Hy+09fOE1LxaNilXwg/86HTXZx4Ua28T6vLu4RwSl4ToKNogTFCMYJLBYbtHGNuUbAL4tYp89SIiBp2l255nrW0FA49ryg7TbiPFIqXq+XEI/nJBS4PFVwHi9IShgtzeXrcIlz1JeCVDCZKqkVIC0AdB04t89/1O/w1cDnyilFU='
        self.__YOUR_CHANNEL_SECRET = '4ea4eac1ae4f9f25b2082dc1d37ac972'
        self.__KEY = '2f42326a4d52784249447133356f656338317a3373464a4c4d6c73506a462f72574331687568694a637641'
        self.__endpoint = 'https://api.apigw.smt.docomo.ne.jp/dialogue/v1/dialogue?APIKEY='
        self.__API_KEY = "b658161bac2942afc45703a43ff1b362"
        self.__api = "http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={key}"

    def get_YCAT(self):
        return self.__YOUR_CHANNEL_ACCESS_TOKEN

    def get_YCS(self):
        return self.__YOUR_CHANNEL_SECRET

    def get_KEY(self):
        return self.__KEY

    def get_endpoint(self):
        return self.__endpoint

    def get_APIKEY(self):
        return self.__API_KEY

    def get_api(self):
        return self.__api


class Push(object):
    def morning_information(self):
        info = Info()
        api = info.get_api()
        API_KEY = info.get_APIKEY()
        city_name = 'Hakodate'
        url = api.format(city=city_name, key=API_KEY)
        print(url)
        response = requests.get(url)
        data = json.loads(response.text)
        K = 273.15
        city = data['name']
        temp = round(data['main']['temp'] - K, 2)
        weather = data["weather"][0]["main"]
        description = data["weather"][0]["description"]
        line1 = "おはよううさ。今日の天気うさ。\n"
        line2 = 'City :' + str(city) + '\n'
        line3 = 'temp :' + str(temp) + '\n'
        line4 = 'weather :' + str(weather) + '\n'
        line5 = 'description : ' + str(description)
        sentence = line1 + line2 + line3 + line4 + line5
        return sentence


