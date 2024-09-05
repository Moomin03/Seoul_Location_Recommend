import requests
import json
import csv
# 사이트에 등록되어 있는 매물이 없을 때 반환하는 값
error = {'name': 'Error', 'code': 404, 'message': ''}
# 메인 코드 (필요한 데이터를 출력)
def data_remix(frame):
    if frame != error:
        # 데이터를 넣어놓을 뼈대
        basic = []
        # 데이터 ID
        _id = frame['item']['itemId']
        basic.append(_id)
        # 건물명
        try:
            _name = frame['danji']['name']
            basic.append(_name)
        except KeyError:
            basic.append('미등록 건물명')
        # 지번 주소
        try:
            _address = frame['item']['jibunAddress']
            basic.append(_address)
        except KeyError:
            _address = frame['item']['addressOrigin']['fullText']
            basic.append(_address)
        # 월세 / 전세
        _saleType = frame['item']['salesType']
        basic.append(_saleType)
        # 오피스텔 / 빌라
        _serviceType = frame['item']['serviceType']
        basic.append(_serviceType)
        # 가격
        _price = frame['item']['price']
        if 'deposit' in frame['item']['price']:
            basic.append(_price['deposit'])
            basic.append(_price['rent'])
        # 관리비
        _manageCost = frame['item']['manageCost']
        basic.append(_manageCost['amount'])
        # 면적
        _area = frame['item']['area']
        basic.append(round(_area['전용면적M2']*0.3025, 1))
        # 근처 지하철역
        _subways = frame['subways']
        if not _subways:
            basic.append("없음")
        else:
            basic.append([i['name'] for i in _subways])
        # 건물 승인 일자
        _approvedDate = frame['item']['approveDate']
        basic.append(_approvedDate)
        # 게시글 수정 날짜
        _updated = frame['item']['updatedAt']
        basic.append(_updated.split(' ')[0])
        # 경도
        _lat = frame['item']['location']['lat']
        basic.append(_lat)
        #위도
        _long = frame['item']['location']['lng']
        basic.append(_long)
        # 결과값 배열로 반환
        return basic
    else:
        pass
def make_file(a, b):
    with open('../home_data5.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        column = ['ID', '건물명', '주소', '판매 유형', '건물 유형', '보증금', '월 납입 비용', '관리비', '면적(단위:평)',
                  '주변 지하철역', '준공일자', '판매등록일자', 'lat', 'long']
        writer.writerow(column)
        for i in range(a, b):
            url = "https://apis.zigbang.com/v3/items/4{:07}?version=&domain=zigbang".format(i)
            res = requests.get(url)
            frame = json.loads(res.text)
            # 데이터 분류 함수 발동
            data = data_remix(frame)
            if data != None:
                writer.writerow(data)
            print(f'-----{i+1}번째 크롤링을 완료했습니다!!-----')