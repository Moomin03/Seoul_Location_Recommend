import requests
from bs4 import BeautifulSoup

class weather_info:
    def __init__(self):
        self.url = 'https://search.daum.net/search?w=tot&DA=YZR&t__nil_searchbox=btn&q=서울+날씨'
        self.res = requests.get(self.url)
        self.soup = BeautifulSoup(self.res.text, 'html.parser')
        self.frame = self.soup.select_one('span.desc_temp')
    def weather_dis(self):
        weather = self.frame.select_one('span.txt_weather').get_text().split(',')[1]
        return weather
    def temper_dis(self):
        temp = self.frame.select_one('strong.txt_temp').get_text()
        return temp

class usmoney_info:
    def __init__(self):
        self.url = 'https://search.daum.net/search?w=tot&m=&q=미국%20기준금리&nzq=기준금리&DA=NSJ'
        self.res = requests.get(self.url)
        self.soup = BeautifulSoup(self.res.text, 'html.parser')
        self.frame = self.soup.select_one('div.wrap_cont')
    def usmoney(self):
        u_money = self.frame.select('dd.cont')[1].get_text().split(' ')[1]
        return u_money

class krmoney_info:
    def __init__(self):
        self.url = 'https://search.daum.net/search?nil_suggest=btn&w=tot&DA=SBC&q=기준금리'
        self.res = requests.get(self.url)
        self.soup = BeautifulSoup(self.res.text, 'html.parser')
        self.frame = self.soup.select_one('div.wrap_cont')
    def krmoney(self):
        k_money = self.frame.select('dd.cont')[1].get_text().split(' ')[1]
        return k_money