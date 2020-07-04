# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import (QMainWindow, QApplication, QFileDialog)
from PyQt5.QtGui import (
    QTextCharFormat,
    QTextCursor,
    QColor,
)
import sys
from Ui_text_editor import Ui_MainWindow
from bloom_filter import BloomFilter
from font_config import FontColor
from file_status import FileStatus
from highlighter import Highlighter

class TextEditor(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()

        # Attribution
        self.ui = Ui_MainWindow()
        self.init_UI()  # 界面绘制交给InitUi方法
        self.file_status = FileStatus()
        self.highlighter = Highlighter(self.ui)

    def init_UI(self):
        self.ui.setupUi(self)
        self.ui.textEdit.setFontPointSize(16)
        self.ui.textEdit.setStyleSheet("background-color:#F5F5F5")
        self.ui.textBrowser.setStyleSheet("background-color:#F5F5F5")
        self.setWindowTitle('未命名')
        self.show()

    # 槽函数
    @pyqtSlot()
    def on_textEdit_textChanged(self):
        # 若有发生更改，更改后光标必定是在被更改处的前面，anchor数值为最后一次输入在文档的下标+1。
        # 所以只需要对每次文本更改后位置到前面遇见空白符为止的字符串进行检验，若前后无符号，则可直接拿去检验；若后面有左括号：[({，则将括号删去。
        if self.highlighter.flag_format_changed:
            self.highlighter.flag_format_changed = False
            return

        self.file_status.set_TextChanged()

        # set windows name
        if not (self.file_status.is_saved or self.file_status.is_saveFlag_setted):
            self.setWindowTitle(self.file_status.filename+'*')
            self.file_status.is_saveFlag_setted = True

        # set font
        if self.file_status.is_openFile:
            self.highlighter.mode_openfile()
        else:
            self.highlighter.mode_normal()

    @pyqtSlot()
    # 打开文件
    def on_act_open_triggered(self):
        filename = QFileDialog.getOpenFileName(self, caption='Open File', directory='./', filter="c files(*.c);; cpp files(*.cpp)")
        if filename[0] == '':
            return
        with open(filename[0], 'r') as f:
            content = ''
            for li in f.readlines():
                content += li
        # file_status
        self.file_status.set_openStatus(filename[0])
        # windows title
        self.setWindowTitle(self.file_status.filename)
        # set_text
        self.ui.textEdit.setText(content)

    @pyqtSlot()
    # 另存为
    def on_act_saveAs_triggered(self):
        filename = QFileDialog.getSaveFileName(self, caption='Open File', directory='./', filter="c files(*.c);; cpp files(*.cpp)")
        if filename[0] == '':
            return
        with open(filename[0], 'w') as f:
            f.write(self.ui.textEdit.document().toPlainText())
        self.setWindowTitle(self.file_status.filename)
        self.file_status.set_saveStatus()

    @pyqtSlot()
    # 保存文件
    def on_act_save_triggered(self):
        if self.file_status.is_untitle:
            self.on_act_saveAs_triggered()
        else:
            with open(self.file_status.filedir, 'w') as f:
                f.write(self.ui.textEdit.document().toPlainText())
                # windows title
                self.setWindowTitle(self.file_status.filename)
                self.file_status.set_saveStatus()

    @pyqtSlot()
    # 新建
    def on_act_new_triggered(self):
        self.ui.textEdit.setText('')
        self.setWindowTitle('未命名')
        self.file_status.__init__()


if __name__ == '__main__':
    # 创建应用程序和对象
    app = QApplication(sys.argv)
    ex = TextEditor()
    sys.exit(app.exec_())
