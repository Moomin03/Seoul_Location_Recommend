import sys
from unittest import removeResult

from PyQt5.QtWidgets import *
from PyQt5 import uic
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import sqlite3

incomeGraph_ui = uic.loadUiType('income_graph.ui')[0]

class IncomeGraph(QMainWindow, incomeGraph_ui):
    def __init__(self, usr_id):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.usr_id = usr_id

        conn = sqlite3.connect('subscriber.db')
        cursor = conn.cursor()
        query = 'SELECT name, total_money, pay FROM subscribers WHERE id=?'
        cursor.execute(query, (self.usr_id,))
        result = cursor.fetchone()
        self.r_name = result[0]
        self.total_money = result[1]
        self.pay = result[2]
        conn.close()

        # 데이터 셋
        self.x = np.arange(1, 21)
        self.base_income = 2228445
        self.y = np.linspace(0.1, 2.0, num=20)*self.base_income
        # 캔버스 그리기
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        # Scatter plot 추가
        self.ax = self.figure.add_subplot(111)
        self.ax.plot(self.x, self.y, 'bo-', label='Standard_Money')
        self.ax.scatter(self.whereami(int(str(self.pay)+'0000')), int(str(self.pay)+'0000'), s=100, marker='^',
                        label='User')
        self.ax.legend()
        # self.ax.scatter(self.x, self.y, marker='bo-')
        self.ax.set_xticks(np.arange(1, 21, 2))
        self.ax.set_xticklabels(f'{i}' for i in np.arange(1, 21, 2))
        self.ax.grid()
        # 레이아웃 설정
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.widget_graph.setLayout(layout)
        self.canvas.draw()

        self.displaying()

    def displaying(self):
        self.ex_label.setText(f'{self.r_name}님의 월 소득은 {self.pay}만원으로 {self.whereami(int(str(self.pay)+"0000"))}분위에 위치합니다.')

    # 나의 위치를 파악할 수 있는 함수
    def whereami(self, data):
        for i in range(1, len(self.y)):
            if self.y[i] > data:
                return i-1
        return len(self.y)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    incomeWindow = IncomeGraph()
    incomeWindow.show()
    app.exec_()


