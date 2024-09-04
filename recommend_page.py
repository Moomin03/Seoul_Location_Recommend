import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import sqlite3

recommend_uic = uic.loadUiType('recommend_ui.ui')[0]
class RecommendPage(QMainWindow, recommend_uic):
    def __init__(self, user_id):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.usr_id = user_id
        self.query = 'SELECT total_money, pay FROM subscribers where id=?'
        self.conn = sqlite3.connect('subscriber.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, (user_id, ))
        self.result = self.cursor.fetchone()
        self.cursor.close()
        self.have_money = self.result[0]
        self.will_money = self.result[1]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    recommend_window = RecommendPage()
    recommend_window.show()
    app.exec_()
