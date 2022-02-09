import sys

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QCursor, QIcon, QColor, QPixmap
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QWidget, QTextEdit, QHBoxLayout, QVBoxLayout, QSplitter, \
     QComboBox, QFileDialog, QApplication

from require.Paintboard import PaintBoard
from require import network


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(self.width(), self.height())
        self.resize(1000, 800)
        self.setWindowTitle('math symbol recognition')
        self.setWindowIcon(QIcon('./icon/math.ico'))
        self.setStyleSheet("background: #161219;")

        self.btn_hand = QPushButton('手写识别', self)
        self.btn_hand.setGeometry(270, 60, 100, 40)
        self.btn_hand.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_hand.setStyleSheet(
            "*{border: 2px groove '#BC006C';" +
            "border-radius: 18px;" +
            "font-size: 20px;" +
            "color: 'white';" +
            "padding: 20px 0;" +
            "margin: 60px 120px}" +
            "*:hover{background: '#BC006C';}"
        )
        self.btn_hand.clicked.connect(self.btn_handwritten_function)

        self.btn_pic = QPushButton('图片识别', self)
        self.btn_pic.setGeometry(270, 140, 100, 40)
        self.btn_pic.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_pic.setStyleSheet(
            "*{border: 2px groove '#BC006C';" +
            "border-radius: 18px;" +
            "font-size: 20px;" +
            "color: 'white';" +
            "padding: 20px 0;" +
            "margin: 60px 120px}" +
            "*:hover{background: '#BC006C';}"
        )
        self.btn_pic.clicked.connect(self.btn_picture_function)

        self.btn_ab = QPushButton('关于', self)
        self.btn_ab.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_ab.setStyleSheet(
            "*{border: 2px groove '#BC006C';" +
            "border-radius: 18px;" +
            "font-size: 20px;" +
            "color: 'white';" +
            "padding: 20px 0;" +
            "margin: 60px 120px}" +
            "*:hover{background: '#BC006C';}"
        )
        self.btn_ab.setGeometry(270, 220, 100, 40)
        self.btn_ab.clicked.connect(self.btn_ab_function)

        self.btn_exit = QPushButton('退出', self)
        self.btn_exit.setGeometry(270, 300, 100, 40)
        self.btn_exit.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_exit.setStyleSheet(
            "*{border: 2px groove '#BC006C';" +
            "border-radius: 18px;" +
            "font-size: 20px;" +
            "color: 'white';" +
            "padding: 20px 0;" +
            "margin: 60px 120px}" +
            "*:hover{background: '#BC006C';}"
        )
        self.btn_exit.clicked.connect(self.btn_close_function)

    def btn_handwritten_function(self):
        self.hide()  # 隐藏此窗口
        self.backtrack = write_recognition()  # 将第二个窗口换个名字
        self.backtrack.show()  # 经第二个窗口显示出来

    def btn_picture_function(self):
        self.hide()  # 隐藏此窗口
        self.backtrack = picture_recognition()
        self.backtrack.show()

    def btn_ab_function(self):
        self.hide()  # 隐藏此窗口
        self.backtrack = about()
        self.backtrack.show()

    def btn_close_function(self):
        self.close()


class write_recognition(QWidget):
    def __init__(self):
        super(write_recognition, self).__init__()
        self.__InitData()
        self.__InitView()

    def __InitData(self):
        self.__paintBoard = PaintBoard(self)
        self.__colorList = QColor.colorNames()

    def __InitView(self):
        self.resize(640, 600)
        self.setFixedSize(self.width(), self.height())
        self.setWindowTitle("Handwritten Recognition")
        self.setWindowIcon(QIcon('./icon/math.ico'))
        self.edit = QTextEdit(self)
        self.edit.setGeometry(500, 100, 120, 100)
        self.edit.setStyleSheet("font-size: 25px")

        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(10)
        main_layout.addWidget(self.__paintBoard)
        sub_layout = QVBoxLayout()
        sub_layout.setContentsMargins(5, 5, 5, 5)

        splitter = QSplitter(self)
        sub_layout.addWidget(splitter)

        self.__btn_Recognize = QPushButton("开始识别")
        self.__btn_Recognize.setParent(self)

        self.__btn_Recognize.clicked.connect(self.btn_rec_function)
        sub_layout.addWidget(self.__btn_Recognize)

        self.__btn_Clear = QPushButton("清空画板")
        self.__btn_Clear.setParent(self)
        self.__btn_Clear.clicked.connect(self.__paintBoard.Clear)
        sub_layout.addWidget(self.__btn_Clear)

        self.__btn_return = QPushButton("返回")
        self.__btn_return.setParent(self)
        self.__btn_return.clicked.connect(self.btn_ret_function)
        sub_layout.addWidget(self.__btn_return)

        self.__btn_Quit = QPushButton("退出")
        self.__btn_Quit.setParent(self)
        self.__btn_Quit.clicked.connect(self.btn_quit_function)
        sub_layout.addWidget(self.__btn_Quit)

        main_layout.addLayout(sub_layout)

    def __fillColorList(self, comboBox):
        index_black = 0
        index = 0
        for color in self.__colorList:
            if color == "black":
                index_black = index
            index += 1
            pix = QPixmap(70, 20)
            pix.fill(QColor(color))
            comboBox.addItem(QIcon(pix), None)
            comboBox.setIconSize(QSize(70, 20))
            comboBox.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        comboBox.setCurrentIndex(index_black)

    def on_PenThicknessChange(self):
        penThickness = self.__spinBox_penThickness.value()
        self.__paintBoard.ChangePenThickness(penThickness)

    def btn_rec_function(self):
        savePath = "./test_img/pic.png"
        image = self.__paintBoard.GetContentAsQImage()
        image.save(savePath)
        image = network.Image.open(savePath).convert('RGB')
        r_image = network.data_transform(image)
        r_image = network.torch.unsqueeze(r_image, dim=0).float()
        output = network.model(r_image)
        pred = output.argmax(dim=1, keepdim=True)
        result = network.symbol_names[int(pred)]
        self.edit.setText('result:\n' + result)

    def btn_ret_function(self):
        self.hide()
        self.backtrack = MainWindow()
        self.backtrack.show()

    def btn_quit_function(self):
        self.close()

class picture_recognition(QWidget):
    def __init__(self):
        super(picture_recognition, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.resize(640, 520)
        self.setFixedSize(self.width(), self.height())
        self.setWindowTitle('图片符号识别')
        self.setWindowIcon(QIcon('./icon/math.ico'))
        self.setStyleSheet("background: #161219;")
        self.label_name5 = QLabel('待载入图片', self)
        self.label_name5.setGeometry(10, 20, 480, 480)
        self.label_name5.setStyleSheet("QLabel{background:white;}"
                                       "QLabel{color:rgb(0,0,0,120);font-size:15px;font-weight:bold;font-family:宋体;}"
                                       )
        self.label_name5.setAlignment(QtCore.Qt.AlignCenter)

        self.edit = QTextEdit(self)
        self.edit.setGeometry(500, 100, 120, 100)
        self.edit.setStyleSheet('color: white;' +
                                "font-size: 25px")

        self.btn_select = QPushButton('选择图片', self)
        self.btn_select.setGeometry(520, 320, 100, 30)
        self.btn_select.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_select.setStyleSheet(
            "*{border: 2px groove '#BC006C';" +
            "border-radius: 18px;" +
            "font-size: 20px;" +
            "color: 'white';" +
            "padding: 20px 0;" +
            "margin: 60px 120px}" +
            "*:hover{background: '#BC006C';}"
        )
        self.btn_select.clicked.connect(self.btn_select_image)

        self.btn_rec = QPushButton('识别图片', self)
        self.btn_rec.setGeometry(520, 370, 100, 30)
        self.btn_rec.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_rec.setStyleSheet(
            "*{border: 2px groove '#BC006C';" +
            "border-radius: 18px;" +
            "font-size: 20px;" +
            "color: 'white';" +
            "padding: 20px 0;" +
            "margin: 60px 120px}" +
            "*:hover{background: '#BC006C';}"
        )
        self.btn_rec.clicked.connect(self.btn_rec_function)

        self.btn_ret = QPushButton('返回', self)
        self.btn_ret.setGeometry(520, 420, 100, 30)
        self.btn_ret.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_ret.setStyleSheet(
            "*{border: 2px groove '#BC006C';" +
            "border-radius: 18px;" +
            "font-size: 20px;" +
            "color: 'white';" +
            "padding: 20px 0;" +
            "margin: 60px 120px}" +
            "*:hover{background: '#BC006C';}"
        )
        self.btn_ret.clicked.connect(self.btn_ret_function)

        self.btn_clo = QPushButton('退出', self)
        self.btn_clo.setGeometry(520, 470, 100, 30)
        self.btn_clo.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_clo.setStyleSheet(
            "*{border: 2px groove '#BC006C';" +
            "border-radius: 18px;" +
            "font-size: 20px;" +
            "color: 'white';" +
            "padding: 20px 0;" +
            "margin: 60px 120px}" +
            "*:hover{background: '#BC006C';}"
        )
        self.btn_clo.clicked.connect(self.btn_clo_function)

    def btn_select_image(self):
        global fname
        imgName, imgType = QFileDialog.getOpenFileName(self, "打开图片", "", "All Files(*)")
        jpg = QtGui.QPixmap(imgName).scaled(self.label_name5.width(), self.label_name5.height())
        self.label_name5.setPixmap(jpg)
        fname = imgName

    def btn_rec_function(self):
        global fname
        image = network.Image.open(fname).convert('RGB')
        r_image = network.data_transform(image)
        r_image = network.torch.unsqueeze(r_image, dim=0).float()
        output = network.model(r_image)
        pred = output.argmax(dim=1, keepdim=True)
        result = network.symbol_names[int(pred)]
        self.edit.setText('result:\n' + result)

    def btn_ret_function(self):
        self.hide()
        self.backtrack = MainWindow()
        self.backtrack.show()

    def btn_clo_function(self):
        self.close()

class about(QWidget):
    def __init__(self):
        super(about, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.resize(640, 520)
        self.setFixedSize(self.width(), self.height())
        self.setWindowTitle('about')
        self.setStyleSheet("background: #161219;")

        self.label_name = QLabel('重庆森林', self)
        self.label_name.setStyleSheet('color: #BC006C;' + "font-size: 30px")
        self.label_name.setGeometry(260, 100, 180, 120)

        self.btn_ret = QPushButton('返回', self)
        self.btn_ret.setGeometry(270, 220, 100, 50)
        self.btn_ret.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_ret.setStyleSheet(
            "*{border: 2px groove '#BC006C';" +
            "border-radius: 18px;" +
            "font-size: 25px;" +
            "color: 'white';" +
            "padding: 20px 0;" +
            "margin: 60px 120px}" +
            "*:hover{background: '#BC006C';}"
        )
        self.btn_ret.clicked.connect(self.btn_ret_function)

        self.btn_clo = QPushButton('退出', self)
        self.btn_clo.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_clo.setStyleSheet(
            "*{border: 2px groove '#BC006C';" +
            "border-radius: 18px;" +
            "font-size: 25px;" +
            "color: 'white';" +
            "padding: 20px 0;" +
            "margin: 60px 120px}" +
            "*:hover{background: '#BC006C';}"
        )
        self.btn_clo.setGeometry(270, 300, 100, 50)
        self.btn_clo.clicked.connect(self.btn_clo_function)

    def btn_ret_function(self):
        self.hide()
        self.backtrack = MainWindow()
        self.backtrack.show()

    def btn_clo_function(self):
        self.close()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
