import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from Income_graph.income_graph import IncomeGraph
from PyQt5.QtCore import QTimer
import time
import sqlite3
from Background.living_tip import livingTip
from Map.map_page import Mapping
from Background.tip_page import Tipcraw
from Recommend_page.recommend_page import RecommendPage
from Crawling.craw_page import CrawPage


afterLogin_ui = uic.loadUiType('/Users/hack/PycharmProjects/Project_1/After_login/After_Login.ui')[0]

class AfMainWindow(QMainWindow, afterLogin_ui):
    def __init__(self, user_id):
        super().__init__()
        self.setupUi(self)
        self.show()
        # 전 페이지에서 user_id를 받아온다.
        self.usr_id = user_id
        # 뉴스 탭 불러오는 클래스
        self.news = livingTip()
        self.tip = Tipcraw()

        # LCD 타이머 설정
        self.lcd_timer = QTimer(self)
        self.lcd_timer.timeout.connect(self.update_lcd)
        self.lcd_timer.start(1000)
        # 깜빡이는 기능 설정
        self.blink_timer = QTimer(self)
        self.blink_timer.timeout.connect(self.blink_colon)
        self.blink_timer.start(500)  # 500ms = 0.5초마다 호출
        self.colon_visible = True
        self.update_lcd()

        # 가장 먼저할것! - 크롤링
        self.crawling_button.clicked.connect(self.open_craw)
        # 소득분위 페이지
        self.m_incgraph.clicked.connect(self.open_incomeGraph)
        # 사용자 데이터 인사~
        self.welcome()
        # 지도 띄우기
        self.good_region.clicked.connect(self.open_map)
        # 추천해주기
        self.recommend_button.clicked.connect(self.open_recommend)

        # 뉴스 블록 처리. label은 for문 사용 불가능
        self.news_label1.setText('1. {}'.format(self.news.news_bre()[0]))
        self.news_label2.setText('2. {}'.format(self.news.news_bre()[1]))
        self.news_label3.setText('3. {}'.format(self.news.news_bre()[2]))
        self.news_label4.setText('4. {}'.format(self.news.news_bre()[3]))
        self.news_label5.setText('5. {}'.format(self.news.news_bre()[4]))
        self.news_label6.setText('6. {}'.format(self.news.news_bre()[5]))
        self.news_label7.setText('7. {}'.format(self.news.news_bre()[6]))
        self.news_label8.setText('8. {}'.format(self.news.news_bre()[7]))
        self.news_label9.setText('9. {}'.format(self.news.news_bre()[8]))
        self.news_label10.setText('10. {}'.format(self.news.news_bre()[9]))
        # 팁 인출
        self.tip_label1.setText('1. {}'.format(self.tip.get_data()[0]))
        self.tip_label2.setText('2. {}'.format(self.tip.get_data()[1]))
        self.tip_label3.setText('3. {}'.format(self.tip.get_data()[2]))
        self.tip_label4.setText('4. {}'.format(self.tip.get_data()[3]))
        self.tip_label5.setText('5. {}'.format(self.tip.get_data()[4]))
        self.tip_label6.setText('6. {}'.format(self.tip.get_data()[5]))
        self.tip_label7.setText('7. {}'.format(self.tip.get_data()[6]))
        self.tip_label8.setText('8. {}'.format(self.tip.get_data()[7]))
        self.tip_label9.setText('9. {}'.format(self.tip.get_data()[8]))
        self.tip_label10.setText('10. {}'.format(self.tip.get_data()[9]))

    # 사용자 인사 함수
    def welcome(self):
        conn = sqlite3.connect('/Users/hack/PycharmProjects/Project_1/subscriber.db')
        cursor = conn.cursor()
        query = 'SELECT name FROM subscribers WHERE id= ?'
        cursor.execute(query, (self.usr_id,))
        result = cursor.fetchone()
        conn.close()
        self.welcome_label.setText(f'{result[0]}님!!! 만나서 반가워요~')

    # craw page
    def open_craw(self):
        self.craw_page = CrawPage()
    # 소득분위 페이지
    def open_incomeGraph(self):
        self.graph_page = IncomeGraph(self.usr_id)
    # 지도 페이지
    def open_map(self):
        self.map_page = Mapping()
    # 추천 페이지
    def open_recommend(self):
        self.recommend_page = RecommendPage(self.usr_id)

    # lcd 칸
    def update_lcd(self):
        current_time = time.strftime('%H:%M')
        if not self.colon_visible:
            current_time = current_time.replace(':', ' ')
        self.lcdNumber.display(current_time)
    # 콜론 깜빡임 제어
    def blink_colon(self):
        self.colon_visible = not self.colon_visible
        self.update_lcd()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = AfMainWindow()
    mainwindow.show()
    app.exec_()