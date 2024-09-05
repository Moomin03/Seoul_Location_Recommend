import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import sqlite3

subscribe_ui = uic.loadUiType('/Users/hack/PycharmProjects/Project_1/Subscribe/subscribe.ui')[0]

class SubScribe(QMainWindow, subscribe_ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.sb_subscribe.clicked.connect(self.printing)
        self.sb_back.clicked.connect(self.bye)
        # sqlite 데이터화
        self.conn = sqlite3.connect('/Users/hack/PycharmProjects/Project_1/subscriber.db')
        self.cursor = self.conn.cursor()
        # 테이블 생성
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS subscribers (
                    name TEXT,
                    id TEXT PRIMARY KEY,
                    pw TEXT,
                    ans TEXT,
                    total_money INT,
                    pay INT,
                    univ TEXT
                )
                ''')
        self.conn.commit()

    def printing(self):
        name = self.sb_nameData.text()
        id = self.sb_idData.text()
        pw = self.sb_passData.text()
        ans = self.sb_ansData.text()
        total_money = self.sb_moneyData.text()
        pay = self.sb_payData.text()
        univ = self.sb_univ.text()
        if name and id and pw and ans and total_money and pay:
            self.cursor.execute('INSERT INTO subscribers (name, id, pw, ans, total_money, pay, univ) VALUES (?, ?, ?, ?, ?, ?, ?)',
                                (name, id, pw, ans, total_money, pay, univ))
            self.conn.commit()
            QMessageBox.information(self, 'Success', 'Data saved successfully!')
        else:
            QMessageBox.warning(self, 'Input Error', 'Please fill in the blank.')

    def bye(self):
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SubScribe()
    window.show()
    app.exec_()