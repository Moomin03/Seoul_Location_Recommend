import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *

craw_page_ui = uic.loadUiType('/Users/hack/PycharmProjects/Project_1/Crawling/craw_page.ui')[0]

class CrawPage(QMainWindow, craw_page_ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.label.setText('''
        안녕하세요! 프로그램 개발자 장홍서라고 합니다.
        2024년 8월 29일부터 만들기 시작해서 벌써 2024년 9월 5일인걸 보면 시간이 정말 빠릅니다.
        뒤이어 쓸 논문에서도 같은 이야기를 하겠지만, 나의 조건에 맞는 집을 구한다는건, 쉽지 않은 일이잖아요?
        그리고 사회경험이 없는 사회초년생들에게는 더욱이 어려울 것이라고 생각했고, 그들에게 조금이라도
        도움이 되었으면 좋겠다는 바람 하나로 이 프로그램을 기획하게 되었습니다.
        개발하는 과정중에 어려웠던 것도 많았고, 제가 원하는 대로 구현이 되지 않을때도 많았지만,
        그냥 재미있다는 이유 하나로, 이 프로그램을 완성할 이유는 충분했던 것 같습니다.
        이 프로그램을 누가 사용할 지는 잘 모르겠지만, 많은 사람들이 이 프로그램을 접해보셨으면 좋겠습니다.
        그래픽 디자인 전공이 아니다보니, GUI는 조금 떨어질 수는 있지만, 그래도 열심히 노력했습니다!
        앞으로 나아가는 청춘들이, 조금 더 좋은 집에서 살았으면 좋겠습니다!''')
if __name__ == '__main__':
    app = QApplication(sys.argv)
    craw_window = CrawPage()
    craw_window.show()
    app.exec_()