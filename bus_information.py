#!/usr/bin/env python3
# coding:utf-8
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime as dt


class BusInfo(object):
    def __init__(self):
        self.url = "http://www.hakobus.jp/result.php?in=165&out=156"
        self.html = urllib.request.urlopen(self.url)
        self.soup = BeautifulSoup(self.html, "html.parser")
        self.bus_late = self.soup('td', width='160')  # 遅延情報
        self.bus_type = self.soup('td', width='140')  # 系統
        self.bus_end = self.soup('td', width='120')   # 終点
        self.bus_time = self.soup('div', align='center')  # バス時刻

    def send_info(self):
        lates = []
        types = []
        ends = []
        times = []
        Bodys = []
        for a in self.bus_late:
            late = str(a)
            late = late.replace('<td width="160">', '')
            late = late.replace('</td>', '')
            if late is '':
                lates.append('無し')
            elif late in '*****':
                lates.append('未定')
            else:
                lates.append(late)

        for a in self.bus_type:
            t = str(a)
            t = t.replace('<td width="140">', '')
            t = t.replace('</td>', '')
            t = t.replace('<div align="center">', '')
            t = t.replace('<br/>', '')
            t = t.replace('\n', '')
            s = t.split(' ')
            t = s[0].replace('<!--', '')
            types.append(t)

        for a in self.bus_end:
            end = str(a)
            end = end.replace('<td width="120">', '')
            end = end.replace('</td>', '')
            end = end.replace('<div align="center">', '')
            end = end.replace('</div>', '')
            ends.append(end)

        for a in self.bus_time:
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
                time = hour+':'+minute
                times.append(time)
            except Exception as e:
                pass

        for i in range(len(lates)):
            Body = [lates[i],  # 遅延
                    types[i],  # 系統
                    ends[i],  # 終点
                    times[i]]  #時刻
            print(Body)
            Bodys.append(Body)
        return Bodys
