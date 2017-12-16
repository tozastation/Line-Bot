#!/usr/bin/env python3
# coding:utf-8
import urllib
from xml.etree import ElementTree
import xml.dom.minidom as md


class Niko(object):
    def __init__(self):
        self.url_ranking = 'http://www.nicovideo.jp/ranking/fav/hourly/sing?rss=2.0&lang=ja-jp'
        self.url_news = 'http://news.nicovideo.jp/categories/10?rss=2.0'
        self.response = urllib.request.urlopen(self.url_ranking)

    def send_niko_list(self, tag):
        root = ElementTree.fromstring(self.response.read())
        document = md.parseString(ElementTree.tostring(root, 'utf-8'))
        list = []
        for a in document.getElementsByTagName(tag):
            list.append(a.toxml().rstrip('</'+tag+'>').lstrip('</'+tag+'>'))

        del list[0]
        return list

