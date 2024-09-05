import requests
from bs4 import BeautifulSoup

class livingTip:
    def __init__(self):
        self.url = 'https://news.naver.com/breakingnews/section/101/260'
        self.res = requests.get(self.url)
        self.soup = BeautifulSoup(self.res.text, 'html.parser')
    def news_bre(self):
        datas = self.soup.select('div.sa_text')
        database = []
        for data in datas:
            database.append(data.select_one('strong.sa_text_strong').get_text())
        return database