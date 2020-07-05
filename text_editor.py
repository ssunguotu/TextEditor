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
from file_status import FileStatus
from highlighter import Highlighter

class TextEditor(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.init_UI()  # 界面绘制交给InitUi方法
        self.file_status = FileStatus()
        self.highlighter = Highlighter(self.ui)

    def init_UI(self):
        self.ui.setupUi(self)
        self.ui.textEdit.setFontPointSize(12)
        self.ui.textEdit.setStyleSheet("background-color:#F5F5F5")
        self.ui.textBrowser.setStyleSheet("background-color:#F5F5F5")
        self.setWindowTitle('未命名')
        self.show()

    @pyqtSlot()
    def on_textEdit_textChanged(self):
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
            self.file_status.is_openFile = False
        else:
            self.highlighter.mode_normal()

    @pyqtSlot()
    # 打开文件
    def on_act_open_triggered(self):
        filename = QFileDialog.getOpenFileName(self, caption='Open File', directory='./', filter="c files(*.c);; cpp files(*.cpp)")
        if filename[0] == '':
            return
        with open(filename[0], 'r', encoding='UTF-8') as f:
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
        with open(filename[0], 'w', encoding='UTF-8') as f:
            f.write(self.ui.textEdit.document().toPlainText())
        self.setWindowTitle(self.file_status.filename)
        self.file_status.set_saveStatus()

    @pyqtSlot()
    # 保存文件
    def on_act_save_triggered(self):
        if self.file_status.is_untitle:
            self.on_act_saveAs_triggered()
        else:
            with open(self.file_status.filedir, 'w', encoding='UTF-8') as f:
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

    @pyqtSlot()
    # 剪切
    def on_act_undo_triggered(self):
        self.ui.textEdit.undo()

    @pyqtSlot()
    # 剪切
    def on_act_cut_triggered(self):
        self.ui.textEdit.cut()

    @pyqtSlot()
    # 复制
    def on_act_copy_triggered(self):
        self.ui.textEdit.copy()

    @pyqtSlot()
    # 粘贴
    def on_act_paste_triggered(self):
        self.ui.textEdit.paste()


if __name__ == '__main__':
    # 创建应用程序和对象
    app = QApplication(sys.argv)
    ex = TextEditor()
    sys.exit(app.exec_())
