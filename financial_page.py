import pandas as pd

class Preparing:
    def __init__(self):
        self.main_data = pd.read_csv('real_homeData.csv')
        self.districts = self.main_data['구'].unique()
        self.jeon_price = []
        self.wol_alot = []
        self.wol_asmall = []
        for district in self.districts:
            goo_data = self.main_data[self.main_data['구'] == district] # 강남구인 지역
            # '전세'와 '월세'의 평균 보증금 계산
            jeon_mean = goo_data[goo_data['판매 유형'] == '전세']['보증금'].mean()
            wol_mean = goo_data[goo_data['판매 유형'] == '월세']['보증금'].mean()
            wol_rent_mean = goo_data[goo_data['판매 유형'] == '월세']['월 납입 비용'].mean()

            # 평균 보증금 및 월 납입 비용을 리스트에 추가
            self.jeon_price.append(jeon_mean if pd.notna(jeon_mean) else 0)
            self.wol_alot.append(wol_mean if pd.notna(wol_mean) else 0)
            self.wol_asmall.append(wol_rent_mean if pd.notna(wol_rent_mean) else 0)

    def dis_jeon_price(self):
        return self.jeon_price
    def dis_wol_alot(self):
        return self.wol_alot
    def dis_wol_asmall(self):
        return self.wol_asmall