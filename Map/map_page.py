import sys
import folium
import pandas as pd
from PyQt5 import uic
from PyQt5.QtWidgets import QVBoxLayout, QMainWindow, QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from folium import Popup

from prepare_data.data_prepare import Preparing

map_uic = uic.loadUiType('/Users/hack/PycharmProjects/Project_1/Map/map_page.ui')[0]

class Mapping(QMainWindow, map_uic):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        # 평균
        self.mean_datas = Preparing()
        self.mean_wol_lot = self.mean_datas.dis_wol_alot()
        self.mean_wol_small= self.mean_datas.dis_wol_asmall()
        self.mean_jeon_lot = self.mean_datas.dis_jeon_price()
        # 각 구 대표 위치 csv
        self.goo_exact_csv = pd.read_csv('/Users/hack/PycharmProjects/Project_1/csv/korea_seoul_goo.csv').sort_values('goo')
        self.goo_exact_lat = self.goo_exact_csv['lat'].to_list()
        self.goo_exact_long = self.goo_exact_csv['long'].to_list()
        self.goo_exact_name = self.goo_exact_csv['goo'].to_list()
        # QWebEngineView 생성
        self.web_view = QWebEngineView()

        # QVBoxLayout을 사용하여 web_view 추가
        layout = QVBoxLayout()
        layout.addWidget(self.web_view)
        self.map_widget.setLayout(layout)

        # 기준이 되는 지도 (서울 시청)
        self.map = folium.Map(location=['37.5663174209601', '126.977829174031'], zoom_start=17)
        folium.Marker(location=['37.5663174209601', '126.977829174031'],
                      icon=folium.Icon(color='blue'),
                      popup='서울 시청').add_to(self.map)
        # 서울 구/동별 위도 경도 데이터 불러오기
        self.total_data = pd.read_csv('/Users/hack/PycharmProjects/Project_1/csv/kr_seoul_dong_loc.csv').dropna(how='any')
        # 각 구가 가지고 있는 데이터 딕셔너리화
        self.goo_data = dict(self.total_data.iloc[:, 0].value_counts())
        # 특정 구만 추출
        self.goo_name = self.total_data['goo'].unique()
        # 색상
        self.colors = ['gray', 'beige', 'green', 'darkblue', 'darkred', 'cadetblue', 'orange', 'blue', 'darkgreen',
                       'lightred', 'purple', 'lightgreen', 'red', 'pink', 'darkpurple', 'white', 'black', 'lightgray',
                       'lightblue', 'gray', 'beige', 'green', 'darkblue', 'darkred', 'cadetblue']
        # 딕셔너리 형태로 25개의 구 데이터를 색상과 매칭
        self.color_map = dict(zip(sorted(self.goo_name), self.colors[:len(self.goo_name)]))
        self.add_marker()
        self.add_more()
        self.draw_map()
        self.load_map()
    def add_marker(self):
        for goo in self.goo_name:
            color = self.color_map[goo]
            goo_data_subset = self.total_data[self.total_data['goo'] == goo]
            for _, row in goo_data_subset.iterrows():
                long = row['long']
                lat = row['lat']
                html_popup = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <style>
                        .popup {{
                            font-family: Arial, sans-serif;
                            color: #333;
                        }}
                        .title {{
                            font-size: 16px;
                            font-weight: bold;
                            color: #007bff;
                        }}
                        .content {{
                            font-size: 14px;
                        }}
                        .footer {{
                            font-size: 12px;
                            color: #555;
                        }}
                    </style>
                </head>
                <body>
                    <div class="popup">
                        <div class="title">서울특별시 {row['dong']}</div>
                    </div>
                </body>
                </html>
                """
                folium.Marker(location=[str(long), str(lat)],
                              icon=folium.Icon(color=color),
                              popup=Popup(html_popup, max_width=300)).add_to(self.map)
                folium.Circle(location=[str(long), str(lat)],
                              fill=True,
                              fill_color=color,
                              radius=100,
                              fill_opacity=0.2).add_to(self.map)
    def add_more(self):
        for i in zip(self.goo_exact_name, self.goo_exact_lat, self.goo_exact_long,
                     self.mean_jeon_lot, self.mean_wol_lot, self.mean_wol_small):
            title = i[0]
            jeon_lot = int(i[3])
            wol_lot = int(i[4])
            wol_lent = int(i[5])
            description = "<tip> 해당 프로그램은 이곳을 {}의 중심으로 판단했습니다.".format(i[0])

            # HTML 팝업 콘텐츠 (f-string 사용)
            html_popup = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    .popup {{
                        font-family: Arial, sans-serif;
                        color: #333;
                    }}
                    .title {{
                        font-size: 16px;
                        font-weight: bold;
                        color: #007bff;
                    }}
                    .content {{
                        font-size: 14px;
                    }}
                    .footer {{
                        font-size: 12px;
                        color: #555;
                    }}
                </style>
            </head>
            <body>
                <div class="popup">
                    <div class="title">서울특별시 {title}</div>
                    <div class="content">
                        <p>{description}</p>
                        <ul>
                            <li>전세 보증금 평균 : {jeon_lot}만원</li>
                            <li>월세 보증금 평균: {wol_lot}만원</li>
                            <li>월세 월임대료 평균 : {wol_lent}만원</li>
                        </ul>
                    </div>
                    <div class="footer">{title} 방문을 환영합니다!</div>
                </div>
            </body>
            </html>
            """
            folium.Marker(
                location=[str(i[1]), str(i[2])],
                popup=folium.Popup(html_popup, max_width=300),
                icon=folium.Icon(color='red')
            ).add_to(self.map)
            folium.Circle(
                location=[str(i[1]), str(i[2])],
                fill=True,
                fill_color='red',
                radius=1000,
                fill_opacity=0.1,
                color='red'
            ).add_to(self.map)

    def load_map(self):
        html_file_path = '/Users/hack/PycharmProjects/Project_1/Map/Seoul_map.html'
        self.web_view.setUrl(QUrl.fromLocalFile(html_file_path))

    def draw_map(self):
        self.map.save('/Users/hack/PycharmProjects/Project_1/Map/Seoul_map.html')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    map_window = Mapping()
    map_window.show()
    app.exec_()