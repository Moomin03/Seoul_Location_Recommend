import pandas as pd
from importlib_resources import files
import re

# 필요한 칼럼
columns = ['ID', '건물명', '주소', '판매 유형', '건물 유형', '보증금', '월 납입 비용',
       '관리비', '면적(단위:평)', '주변 지하철역', '준공일자', '판매등록일자']
# 정제되지 않은 모든 데이터
unfiltered_data = pd.read_csv('home_data.csv')[columns]
# 해당 주소값에 서울 구에 대한 정보가 포함되는지 판별 리스트
unfiltered_address = unfiltered_data['주소'].to_list()
# 서울시 구, 동 데이터
goo_dong_data = pd.read_csv('seoul.csv')
seoul_goo_districts = goo_dong_data['goo'].unique()
seoul_dong_districts = goo_dong_data['dong'].dropna().unique()
# 주소를 넣으면 각 구가 들어있는지 판별하는 함수
def seoul_districts(address):
    return any(district in address for district in seoul_goo_districts)
# 필터링을 거친 리스트열, 불리언이라서 unfiltered_data에 넣어야됨
filtered_boolen = [True if seoul_districts(address=address) else False for address in unfiltered_address]
filtered_data = unfiltered_data[filtered_boolen]
# 각 데이터가 어떤 구인지, 어떤 동인지 해당 값을 데이터 프레임에 새로운 열 추가
def extract_goo(address):
    for district in seoul_goo_districts:
        if district in address:
            return district
    return None
filtered_data['구'] = filtered_data['주소'].apply(extract_goo)
# 정규 표현식 패턴 생성
dong_patterns = [re.compile(r'\b' + re.escape(district) + r'\b') for district in seoul_dong_districts]
# 정확한 동 이름을 추출하는 함수
def extract_dong(address):
    for pattern in dong_patterns:
        match = pattern.search(address)
        if match:
            return match.group()
    return None
filtered_data['동'] = filtered_data['주소'].apply(extract_dong)
filtered_data = filtered_data.sort_values('구')
filtered_data.to_csv('real_homeData.csv')