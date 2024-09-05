import pandas as pd
import re

class Preparing:
    def __init__(self):
        self.columns = ['ID', '건물명', '주소', '판매 유형', '건물 유형', '보증금', '월 납입 비용',
                        '관리비', '면적(단위:평)', '주변 지하철역', '준공일자', '판매등록일자', 'lat', 'long']
        # 정제되지 않은 모든 데이터
        self.unfiltered_data = pd.read_csv('/Users/hack/PycharmProjects/Project_1/csv/FRAME.csv')[self.columns]
        # 해당 주소값에 서울 구에 대한 정보가 포함되는지 판별 리스트
        self.unfiltered_address = self.unfiltered_data['주소'].to_list()
        # 서울시 구, 동 데이터
        self.goo_dong_data = pd.read_csv('/Users/hack/PycharmProjects/Project_1/csv/kr_seoul_dong_loc.csv')
        self.seoul_goo_districts = self.goo_dong_data['goo'].unique()
        self.seoul_dong_districts = self.goo_dong_data['dong'].dropna().unique()
        # 필터링을 거친 리스트열, 불리언이라서 unfiltered_data에 넣어야됨
        self.filtered_boolen = [True if self.kr_seoul_goo_districts(address=address) else False for address in self.unfiltered_address]
        self.filtered_data = self.unfiltered_data[self.filtered_boolen]
        self.filtered_data['구'] = self.filtered_data['주소'].apply(self.extract_goo)

        # 정규 표현식 패턴 생성
        self.dong_patterns = [re.compile(r'\b' + re.escape(district) + r'\b') for district in self.seoul_dong_districts]
        self.filtered_data['동'] = self.filtered_data['주소'].apply(self.extract_dong)
        self.filtered_data = self.filtered_data.sort_values('구')

        self.districts = self.filtered_data['구'].unique()
        self.jeon_price = []
        self.wol_alot = []
        self.wol_asmall = []
        for district in self.districts:
            goo_data = self.filtered_data[self.filtered_data['구'] == district]  # 강남구인 지역
            # '전세'와 '월세'의 평균 보증금 계산
            jeon_mean = goo_data[goo_data['판매 유형'] == '전세']['보증금'].mean()
            wol_mean = goo_data[goo_data['판매 유형'] == '월세']['보증금'].mean()
            wol_rent_mean = goo_data[goo_data['판매 유형'] == '월세']['월 납입 비용'].mean()

            # 평균 보증금 및 월 납입 비용을 리스트에 추가
            self.jeon_price.append(jeon_mean if pd.notna(jeon_mean) else 0)
            self.wol_alot.append(wol_mean if pd.notna(wol_mean) else 0)
            self.wol_asmall.append(wol_rent_mean if pd.notna(wol_rent_mean) else 0)

    def kr_seoul_goo_districts(self, address):
        return any(district in address for district in self.seoul_goo_districts)
    def extract_goo(self, address):
        for district in self.seoul_goo_districts:
            if district in address:
                return district
        return None
    # 정확한 동 이름을 추출하는 함수
    def extract_dong(self, address):
        for pattern in self.dong_patterns:
            match = pattern.search(address)
            if match:
                return match.group()
        return None
    # 평균 데이터 호출 함수
    def dis_jeon_price(self):
        return self.jeon_price
    def dis_wol_alot(self):
        return self.wol_alot
    def dis_wol_asmall(self):
        return self.wol_asmall
    def return_data(self):
        return self.filtered_data






