import sqlite3
from prepare_data.data_prepare import Preparing
class RecommendLocation:
    def __init__(self, user_id):
        self.user_id = user_id
        self.prepared_data = Preparing()
        self.conn = sqlite3.connect('/Users/hack/PycharmProjects/Project_1/subscriber.db')
        self.cursor = self.conn.cursor()
        self.query = "SELECT total_money, pay FROM subscribers WHERE id=?"
        self.cursor.execute(self.query, (self.user_id,))
        self.decode_data = self.cursor.fetchone()
        self.conn.close()
        self.total_money = self.decode_data[0]
        self.pay = int(str(self.decode_data[1])+'0000')

        self.total_homedata = self.prepared_data.return_data().dropna()
        self.need_data = self.total_homedata[['주소', '판매 유형', '보증금', '월 납입 비용', '관리비', '면적(단위:평)', 'lat', 'long', '구', '동']]
        self.bo_money = self.need_data['보증금'].to_list()
        self.wol_money = self.need_data['월 납입 비용'].to_list()
        self.need_data['HAI'] = self.need_data.apply(self.self_hai, axis=1)

    def self_hai(self, row):
        real_lent = int(str(int(row['보증금'])) + '0000')
        real_have = int(str(self.total_money)+'0000')
        if real_lent>real_have:
            left_over = real_lent - real_have
            interest_ratio = 0.02
            month_interest_ratio = interest_ratio/12
            year = 20
            every_month = year*12
            wol_money = int(str(int(row['월 납입 비용']))+'0000')
            hai = int((left_over*month_interest_ratio)/round((1-(1+month_interest_ratio)**-every_month), 5)+wol_money)/self.pay*100
            return round(hai, 3)
        else:
            wol_money = int(str(int(row['월 납입 비용'])) + '0000')
            hai = wol_money/self.pay*100
            return round(hai, 3)
    def result(self):
        return self.need_data[self.need_data['HAI']<30]