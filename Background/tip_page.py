import requests
from bs4 import BeautifulSoup

class Tipcraw:
    def __init__(self):
        self.url = 'https://land.naver.com'
        self.res = requests.get(self.url)
        self.soup = BeautifulSoup(self.res.text, 'html.parser')
        self.frame = self.soup.select_one('ul.item_list')
    def get_data(self):
        text_datas = self.frame.select('span.text')
        text_result = []
        for text_data in text_datas:
            text_result.append(text_data.get_text())
        return text_result
    def get_href(self):
        href_datas = self.frame.select('a')
        href_result = []
        for href_data in href_datas:
            href_result.append(href_data.attrs['href'])
        return href_result