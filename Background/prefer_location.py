import requests
import sqlite3

class PreferLocation:
    def __init__(self, user_id):
        self.user_id = user_id
        self.conn = sqlite3.connect('/Users/hack/PycharmProjects/Project_1/subscriber.db')
        self.cursor = self.conn.cursor()
        self.query = "SELECT univ FROM subscribers WHERE id=?"
        self.cursor.execute(self.query, (self.user_id,))
        self.decode_data = self.cursor.fetchone()[0]
        self.conn.close()
        # 크롤링
        self.url = "https://dapi.kakao.com/v2/local/search/keyword.json"
        self.headers = {"Authorization": 'KakaoAK 3732ee66ab6b81c392638300d3eebbe7'}
        self.query = {'query':f'{self.decode_data}'}
        self.result = requests.get(url=self.url,
                                    headers=self.headers,
                                    data=self.query).json()
        self.lat = self.result['documents'][0]['y']
        self.long = self.result['documents'][0]['x']
    def current_lat(self):
        return self.lat
    def current_long(self):
        return self.long
    def current_loc(self):
        return self.decode_data