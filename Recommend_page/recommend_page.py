import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from Recommend_page.recommend_locaton import RecommendLocation
from Background.prefer_location import PreferLocation
from PyQt5.QtWebEngineWidgets import QWebEngineView
import folium
from PyQt5.QtCore import QUrl


recommend_uic = uic.loadUiType('/Users/hack/PycharmProjects/Project_1/Recommend_page/recommend_ui.ui')[0]
class RecommendPage(QMainWindow, recommend_uic):
    def __init__(self, user_id):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.user_id = user_id
        self.recommend_data = RecommendLocation(self.user_id).result().sort_values('HAI')
        self.prefer_lat = PreferLocation(self.user_id).current_lat()
        self.prefer_long = PreferLocation(self.user_id).current_long()
        self.prefer_name = PreferLocation(self.user_id).current_loc()

        self.recommend_1.setText(self.recommend_data.iloc[0]['구'])
        self.recommend_2.setText(self.recommend_data.iloc[1]['구'])
        self.recommend_3.setText(self.recommend_data.iloc[2]['구'])
        self.recommend_4.setText(self.recommend_data.iloc[3]['구'])
        self.recommend_5.setText(self.recommend_data.iloc[4]['구'])
        self.recommend_6.setText(self.recommend_data.iloc[5]['구'])

        self.recommen_1.setText(self.recommend_data.iloc[0]['동'])
        self.recommen_2.setText(self.recommend_data.iloc[1]['동'])
        self.recommen_3.setText(self.recommend_data.iloc[2]['동'])
        self.recommen_4.setText(self.recommend_data.iloc[3]['동'])
        self.recommen_5.setText(self.recommend_data.iloc[4]['동'])
        self.recommen_6.setText(self.recommend_data.iloc[5]['동'])
        # QWebEngineView 생성
        self.web_view = QWebEngineView()
        # QVBoxLayout을 사용하여 web_view 추가
        layout = QVBoxLayout()
        layout.addWidget(self.web_view)
        self.map_widget.setLayout(layout)
        # 기준이 되는 지도 (사용자 지정 주소)
        self.map = folium.Map(location=[str(self.prefer_lat), str(self.prefer_long)], zoom_start=20)
        folium.Marker(location=[str(self.prefer_lat), str(self.prefer_long)],
                      icon=folium.Icon(color='red'),
                      popup=folium.Popup(f'<div onclick="showMessage()">\
                                <h3>{self.prefer_name}</h3>\
                                <p>Click here to see more information.</p>\
                             </div>', max_width=300)).add_to(self.map)
        self.recommend_map()
        self.draw_map()
        self.load_map()

    def load_map(self):
        html_file_path = '/Users/hack/PycharmProjects/Project_1/Recommend_page/result_page.html'
        self.web_view.setUrl(QUrl.fromLocalFile(html_file_path))
    def recommend_map(self):
        for _, row in self.recommend_data.iterrows():
            address = row['주소']
            sale_type = row['판매 유형']
            bo_money = row['보증금']
            wol_pay = row['월 납입 비용']
            mange = row['관리비']
            area = row['면적(단위:평)']
            lat = row['lat']
            long = row['long']
            hai = row['HAI']
            goo = row['구']
            dong = row['동']
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
                                <div class="title">서울특별시 {goo} {dong}</div>
                                <div class="content">
                                    <p>Hello</p>
                                    <ul>
                                        <li>주소 : {address}</li>
                                        <li>판매 유형 : {sale_type}</li>
                                        <li>평수 : {area}평</li>
                                        <li>보증금 : {bo_money}만원</li>
                                        <li>월세 : {wol_pay}만원</li>
                                        <li>관리비 : {mange}만원</li>
                                        <li>HAI : {hai}</li>
                                    </ul>
                                </div>
                                <div class="footer">{goo} {dong} 방문을 환영합니다!</div>
                            </div>
                        </body>
                        </html>
                        """
            folium.Marker(location=[str(lat), str(long)],
                          icon=folium.Icon(color='blue'),
                          popup=folium.Popup(html_popup, max_width=300)).add_to(self.map)
            folium.Circle(location=[str(lat), str(long)],
                          radius=10,
                          color='blue',
                          fil_color='blue',
                          fill_opacity=0.05).add_to(self.map)

    def draw_map(self):
        self.map.save('/Users/hack/PycharmProjects/Project_1/Recommend_page/result_page.html')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    recommend_window = RecommendPage()
    recommend_window.show()
    app.exec_()
