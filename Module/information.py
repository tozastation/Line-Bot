#!/usr/bin/env python3
# coding:utf-8
import json
import os
import requests


class Info(object):
    def __init__(self):
        self.__YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
        self.__YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]
        self.__DOCOMO_API_KEY = os.environ["DOCOMO_API_KEY"]
        self.__DOCOMO_ENDPOINT = "https://api.apigw.smt.docomo.ne.jp/dialogue/v1/dialogue?APIKEY="
        self.__WEATHER_API_KEY = os.environ["WEATHER_API_KEY"]
        self.__WEATHER_API = "http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={key}"

    def get_ycat(self):
        return self.__YOUR_CHANNEL_ACCESS_TOKEN

    def get_ycs(self):
        return self.__YOUR_CHANNEL_SECRET

    def get_docomo_api_key(self):
        return self.__DOCOMO_API_KEY

    def get_docomo_endpoint(self):
        return self.__DOCOMO_ENDPOINT

    def get_weather_api_key(self):
        return self.__WEATHER_API_KEY

    def get_weather_api(self):
        return self.__WEATHER_API

    def morning_information(self):
        api = self.get_weather_api()
        api_key = self.get_weather_api_key()
        city_name = 'Hakodate'
        url = api.format(city=city_name, key=api_key)
        response = requests.get(url)
        data = json.loads(response.text)
        K = 273.15
        city = data['name']
        temp = round(data['main']['temp'] - K, 2)  # 四捨五入
        weather = data["weather"][0]["main"]
        description = data["weather"][0]["description"]
        line1 = "おはよううさ〜。今日の天気うさ。\n"
        line2 = 'City : ' + str(city) + '\n'
        line3 = 'temp : ' + str(temp) + '\n'
        line4 = 'weather : ' + str(weather) + '\n'
        line5 = 'description : ' + str(description)+ '\n'
        line6 = '気をつけて行きやがれうさ。'
        sentence = line1 + line2 + line3 + line4 + line5 + line6
        return sentence

