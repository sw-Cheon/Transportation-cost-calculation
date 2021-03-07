from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel,QGridLayout,QCheckBox,QMenu, QVBoxLayout, QHBoxLayout, \
     QGroupBox, QLineEdit, QPushButton, QTextEdit, QComboBox, QSlider, QInputDialog
from PyQt5.QtGui import QPixmap,QImage,QColor
from PyQt5.QtCore import QDir, Qt,QRect,QSize, QCoreApplication
import socket
import time
import sys
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread, QRect
import os
import threading
from tcc_cls import *

class Ui_TccDialog(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        self.tcc = None
        self.cnt = 0
        self.FLAG_FE_ERROR = False
        self.FLAG_OC_ERROR = False

    def initUI(self):
        self.setWindowTitle('Transportation cost calculation')
        hbox = QHBoxLayout()
        vb = QVBoxLayout()
        vb.addLayout(self.createInfoGroup())
        vb.addLayout(hbox)
        self.setLayout(vb)
        self.show()
       
    def createInfoGroup(self):
        box = QHBoxLayout()
        self.btn = QPushButton('설명보기')
        self.btn.clicked.connect(self.get_Help_Info)
        box.addWidget(self.btn)
        self.btn2 = QPushButton('바로이용')
        self.btn2.clicked.connect(self.get_Oil_Cost)
        box.addWidget(self.btn2)
        self.btn3 = QPushButton('다음')
        self.btn3.clicked.connect(self.next)
        box.addWidget(self.btn3)

        self.infomsg = QTextEdit()
        self.infomsg.setFixedWidth(400)
        self.infomsg.setFixedHeight(400)
        self.infomsg.setStyleSheet("background-color: black; border: 1px solid gray;")
        self.infomsg.setTextColor(QColor(255,255,0))
        self.infomsg.append(' Deerworld의 교통비 산출 프로그램입니다.')
        self.infomsg.append(" 이용을 원하는 메뉴를 선택해주세요.")

        cbox = QHBoxLayout()
        vbox = QVBoxLayout()        
        vbox.addLayout(box)
        vbox.addLayout(cbox)
        vbox.addWidget(self.infomsg)
        return vbox

### Functions # ====================================================================================================== #
    def get_Help_Info(self):
        self.cnt = 1
        self.infomsg.clear()
        self.infomsg.append(" 1. 아래에 있는 url을 복사하고 인터넷 url창에\n     입력하여 Kakao map을 실행해 주세요.")
        self.infomsg.append("   ============================================\n    https://m.map.kakao.com/actions/routeView\n   ============================================")
        self.infomsg.append("\n 2. 출발지와 도착지를 입력하고\n     자동차 아이콘을 눌러 자동차경로 찾기를 합니다.")
        self.infomsg.append("\n 3. 화면이 바뀌면 해당 화면의 url을 복사합니다.")
        self.infomsg.append("\n 4. 3번이 끝났으면 '바로이용'버튼을 눌러주세요!")

    def get_Oil_Cost(self):
        self.cnt = 2
        self.infomsg.clear()
        if (self.FLAG_OC_ERROR == False):
            pass
        else:
            self.infomsg.append(" 잘못된 형식이 입력되었습니다. 다시 입력해주세요.\n")
        self.infomsg.append(" 현재 유가를 가져올 유종을 선택하세요.")
        self.infomsg.append(" 1. 휘발유")
        self.infomsg.append(" 2. 경유")
        self.infomsg.append(" 3. 직접 입력")
        num, ok = QInputDialog.getText(self, '연료 종류', '연료 종류를 입력하세요.')
        if ok:
            if (num == "1" or num == "2" or num == "3"):
                if (num == "3"):
                    oil_Cost, ok = QInputDialog.getText(self, '연료비 입력', '연료비를 입력하세요.')
                    if ok:
                        try:
                            self.tcc.oil_Cost = float(oil_Cost)
                            self.FLAG_OC_ERROR = False
                            self.infomsg.append(" \n 입력된 유가입니다 : " + str(oil_Cost) + '원')
                            self.infomsg.append(" \n 계속 진행하시려면 다음을 눌러주세요.")
                        except:
                            self.FLAG_OC_ERROR = True
                            self.get_Oil_Cost()
                else:
                    self.FLAG_OC_ERROR = False
                    oil_Cost = self.tcc.get_Oil_Information(num) # 4번 이런거 넣었을 때 대처, 3번 직접 입력 눌렀을 때 팝업창.
                    self.infomsg.append(" \n 조회된 유가입니다 : " + str(oil_Cost) + '원')
                    self.infomsg.append(" \n 계속 진행하시려면 다음을 눌러주세요.")
            else:
                self.FLAG_OC_ERROR = True
                self.get_Oil_Cost()

    def get_Fuel_Efficiency(self):
        self.cnt = 3
        self.infomsg.clear()
        if (self.FLAG_FE_ERROR == False):
            self.infomsg.append(" 차량의 도로별 연비를 입력해주세요.")
        else:
            self.infomsg.append(" 연비의 형식이 잘못되었습니다. 다시 입력해주세요.")
        try:
            fe, ok = QInputDialog.getText(self, '일반도로', '일반도로 연비를 입력하세요.')
            if ok:
                self.infomsg.append(" 입력된 일반도로 연비 : {}".format(fe))
                self.tcc.general_Road_Fuel_Efficiency = float(fe)
                self.FLAG_FE_ERROR = False
            fe, ok = QInputDialog.getText(self, '고속도로', '고속도로 연비를 입력하세요.')
            if ok:
                self.infomsg.append(" 입력된 고속도로 연비 : {}".format(fe))
                self.tcc.highway_Fuel_Efficiency = float(fe)
                self.FLAG_FE_ERROR = False
            self.infomsg.append(" \n 계속 진행하시려면 다음을 눌러주세요.")
        except:
            self.FLAG_FE_ERROR = True
            self.get_Fuel_Efficiency()


    def run_Program(self):
        self.infomsg.clear()
        self.infomsg.append(" 복사한 url을 팝업창에 붙여넣기 해주세요.")
        url, ok = QInputDialog.getText(self, '길찾기 url', '길찾기 url을 입력하세요.')
        if ok:
            self.tcc.url = url
            self.infomsg.append("\n > Now calculating...\n")
            # try:
            str_ = self.tcc.run()
            # except:
            #     self.infomsg.clear()
            #     self.infomsg.append(" 잘못된 형식입니다. url을 확인해주세요.")
            #     url, ok = QInputDialog.getText(self, '길찾기 url', '길찾기 url을 입력하세요.')
            #     if ok:
            #         self.tcc.url = url
            #         self.infomsg.append("\n > Now calculating...\n")
            #         str_ = self.tcc.run()
            #         self.infomsg.clear()
            #         self.infomsg.append(str_[0])
            #         self.infomsg.append(str_[1])
            #         self.infomsg.append(str_[2])
            #         self.infomsg.append(str_[3])
            #         self.infomsg.append(str_[4])
            #         self.infomsg.append(str_[5])
            self.infomsg.clear()
            self.infomsg.append(str_[0])
            self.infomsg.append(str_[1])
            self.infomsg.append(str_[2])
            self.infomsg.append(str_[3])
            self.infomsg.append(str_[4])
            self.infomsg.append(str_[5])

        self.infomsg.append("\n 다시 이용하시려면 '바로이용' 버튼을 눌러주세요.")


    def next(self):
        if (self.cnt == 2):
            self.get_Fuel_Efficiency()
        elif (self.cnt == 3):
            self.run_Program()

# ==================================================================================================================== #

### Thread # ========================================================================================================= #
    def run_TCC(self):
        self.tcc = transportation_Cost_Calculation()
# ==================================================================================================================== #

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Ui_TccDialog()
    ui.run_TCC()
    sys.exit(app.exec_())
