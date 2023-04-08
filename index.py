import sys

from PIL import Image
import matplotlib.pyplot as plt
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QColor, QPixmap, QKeySequence
from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QLabel, QWidget, QTextEdit, QHBoxLayout, QVBoxLayout,
    QSplitter, QComboBox, QFileDialog, QApplication, QMessageBox, QShortcut, QMenu)

from require import network
from require.Paintboard import PaintBoard

global file_name, result


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.init_ui()

    def init_ui(self) -> None:
        self.resize(795, 520)
        # self.setFixedSize(self.width(), self.height())
        self.setWindowTitle('math symbol recognition')
        self.setWindowIcon(QIcon('./icon/math.ico'))

        self.label_pic = QLabel('ctrl+1: 选择图片\n'
                                'ctrl+2: 识别图片\n'
                                'ctrl+3: 显示图片\n'
                                'ctrl+4: 程序说明\n'
                                'ctrl+5: 退出程序', self)
        self.label_pic.setGeometry(5, 27, 390, 300)
        self.label_pic.setStyleSheet("QLabel{background:gray;}"
                                     "QLabel{color:rgb(0,0,0,120);font-size:20px;font-weight:bold;font-family:黑体;}"
                                     )
        self.label_pic.setAlignment(QtCore.Qt.AlignCenter)

        self.label_mat_pic = QLabel('ctrl+1: 选择图片\n'
                                    'ctrl+2: 识别图片\n'
                                    'ctrl+3: 显示图片\n'
                                    'ctrl+4: 程序说明\n'
                                    'ctrl+5: 退出程序', self)
        self.label_mat_pic.setGeometry(400, 27, 390, 300)
        self.label_mat_pic.setStyleSheet("QLabel{background:gray;}"
                                         "QLabel{color:rgb(0,0,0,120);font-size:20px;font-weight:bold;font-family:黑体;}"
                                         )
        self.label_mat_pic.setAlignment(QtCore.Qt.AlignCenter)

        self.file_menu = QMenu('file', self)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.file_menu)
        self.file_menu.addAction('open', self.slot_btn_open)
        self.file_menu.addAction('recognize', self.slot_btn_rec)
        self.file_menu.addAction('show', self.slot_btn_show)
        self.file_menu.addAction('write', self.slot_btn_write)

        self.help_menu = QMenu('help', self)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.help_menu)
        self.help_menu.addAction('about', self.slot_btn_about)
        self.help_menu.addAction('close', self.slot_btn_close)

        QShortcut(QKeySequence(self.tr("Ctrl+1")), self, self.slot_btn_open)
        QShortcut(QKeySequence(self.tr("Ctrl+2")), self, self.slot_btn_rec)
        QShortcut(QKeySequence(self.tr("Ctrl+3")), self, self.slot_btn_show)
        QShortcut(QKeySequence(self.tr("Ctrl+4")), self, self.slot_btn_about)
        QShortcut(QKeySequence(self.tr("Ctrl+5")), self, self.slot_btn_close)
        QShortcut(QKeySequence(self.tr("Ctrl+w")), self, self.slot_btn_write)

        self.exp = QTextEdit(self)
        self.exp.setGeometry(180, 360, 420, 150)
        self.exp.setStyleSheet("font-size: 40px")

    def slot_btn_open(self) -> None:
        global file_name
        imgName, imgType = QFileDialog.getOpenFileName(self, "open image", "", "All Files(*)")
        img = QtGui.QPixmap(imgName).scaled(self.label_pic.width(), self.label_pic.height())
        self.label_pic.setPixmap(img)
        file_name = imgName

    def slot_btn_rec(self) -> None:
        global file_name, result
        try:
            image = Image.open(file_name).convert('RGB')
            r_image = network.data_transform(image)
            r_image = network.torch.unsqueeze(r_image, dim=0).float()
            output = network.model(r_image)
            pred = output.argmax(dim=1, keepdim=True)
            result = network.symbol_names[int(pred)]
            self.exp.setText(result)
        except:
            QMessageBox.information(self, 'error', 'No image!\nif u need help\npress ctrl+4')

    def slot_btn_show(self) -> None:
        fig = plt.figure(figsize=(4, 4))
        axes = fig.add_subplot(111)
        axes.set_xticks([])
        axes.set_yticks([])
        axes.spines['left'].set_color('none')
        axes.spines['right'].set_color('none')
        axes.spines['bottom'].set_color('none')
        axes.spines['top'].set_color('none')
        try:
            prediction_image = '$' + result + '$'
            axes.text(0, 0.5, prediction_image, fontsize=20)
            test_pic = './test_img/matplotlib_pic/test.png'
            plt.savefig(test_pic)
            jpg = QtGui.QPixmap(test_pic).scaled(self.label_mat_pic.width(), self.label_mat_pic.height())
            self.label_mat_pic.setPixmap(jpg)
        except:
            QMessageBox.information(self, 'error', 'No image!\nif u need help\npress ctrl+4')

    def slot_btn_about(self) -> None:
        QMessageBox.about(
            self,
            "about",
            "<font size='4' color='pink'>"
            "This is a program that recognize handwritten mathematical symbols.<hr>"
            "Press Ctrl + 1 to open the picture<br>"
            "Press Ctrl + 2 to recognize the picture<br>"
            "Press Ctrl + 3 to display the picture<br>"
            "Press Ctrl + 5 to exit the program<hr>"
            "</font>")

    def slot_btn_close(self) -> None:
        self.close()

    def slot_btn_write(self) -> None:
        self.hide()
        self.backtrack = write_recognition()
        self.backtrack.show()

    def btn_close_function(self) -> None:
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
        image = Image.open(savePath).convert('RGB')
        r_image = network.data_transform(image)
        r_image = network.torch.unsqueeze(r_image, dim=0).float()
        output = network.model(r_image)
        pred = output.argmax(dim=1, keepdim=True)
        result = network.symbol_names[int(pred)]
        self.edit.setText(result)

    def btn_ret_function(self):
        self.hide()
        self.backtrack = MainWindow()
        self.backtrack.show()

    def btn_quit_function(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
