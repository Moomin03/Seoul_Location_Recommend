import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from Subscribe.Subscribe import SubScribe
from Background.main_topdata import weather_info, usmoney_info, krmoney_info
from PyQt5.QtCore import QTimer
import time
import sqlite3
from After_login.After_login import AfMainWindow
from Background.tip_page import Tipcraw
from Background.living_tip import livingTip

main_ui = uic.loadUiType('/Users/hack/PycharmProjects/Project_1/Main/main.ui')[0]

class MainWindow(QMainWindow, main_ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 다른 파일에서 가져오는 클래스
        self.weather = weather_info()
        self.usmoney = usmoney_info()
        self.krmoney = krmoney_info()

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
        # 뉴스 탭 불러오는 클래스
        self.news = livingTip()
        self.tip = Tipcraw()

        self.loginButton.clicked.connect(self.isitright)
        self.subscribe_button.clicked.connect(self.open_subscribe)
        self.m_weather.setText(self.weather.weather_dis())
        self.m_temp.setText(self.weather.temper_dis())
        self.us_money.setText(self.usmoney.usmoney())
        self.kr_money.setText(self.krmoney.krmoney())

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

    # 회원가입 페이지
    def open_subscribe(self):
        self.subscribe_page = SubScribe()
    # 사용자 확인
    def isitright(self):
        id = self.id_input.toPlainText()
        pw = self.pw_input.toPlainText()
        # 데이터베이스 파일에 연결
        conn = sqlite3.connect('/Users/hack/PycharmProjects/Project_1/subscriber.db')
        cursor = conn.cursor()
        # SQL 쿼리 작성
        query = "SELECT * FROM subscribers WHERE id = ? AND pw = ?"
        # 쿼리 실행
        cursor.execute(query, (id, pw))
        # 쿼리 결과 가져오기
        result = cursor.fetchone()
        # 연결 종료
        conn.close()
        # 결과 반환
        if result:
            QMessageBox.information(self, 'Success', '환영합니다!')
            self.openAfterpage(id) # ID와 비밀번호가 일치
        else:
            QMessageBox.information(self, 'Fail', '존재하지 않는 계정입니다!')

    def openAfterpage(self, id):
        self.after_login_window = AfMainWindow(id)
        self.close()
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
    mainwindow = MainWindow()
    mainwindow.show()
    app.exec_()