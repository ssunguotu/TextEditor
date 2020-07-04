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

class TextEditor(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()

        # Attribution
        self.ui = Ui_MainWindow()
        self.keyword_filter = BloomFilter()
        self.type_filter = BloomFilter()
        self.color = FontColor()
        self.file_status = FileStatus()

        # flag
        self.flag_format_changed = False  # 解决无限递归问题
        self.plainFmt = None  # 解决format错误的问题
        # TODO: 封装成类

        # methods 
        self.init_UI()  # 界面绘制交给InitUi方法
        self.init_filter()

    def init_UI(self):
        self.ui.setupUi(self)
        self.ui.textEdit.setFontPointSize(16)
        self.plainFmt = self.ui.textEdit.currentCharFormat()
        self.ui.textEdit.setStyleSheet("background-color:#F5F5F5")
        self.ui.textBrowser.setStyleSheet("background-color:#F5F5F5")
        self.setWindowTitle('未命名')
        self.show()

    def init_filter(self):
        with open('cpp.txt', 'r') as f:
            allword = [li.split()[0] for li in f.readlines()]
        self.keyword_filter.input(allword)
        # self.keyword_filter.input(['using', 'namespace', 'return'])
        self.type_filter.input(['double', 'int', 'char'])

    # Highlighter
    def paint_text(self, lo, hi, color):
        """
        根据所给的参数在textEdit上对颜色进行修改
        lo：要改变颜色的字符串的开始下标
        hi：结束下标
        color：QColor对象，表示颜色
        """
        if hi <= lo:
            return
        self.flag_format_changed = True
        cursor = self.ui.textEdit.textCursor()
        cursor.setPosition(lo, QTextCursor.MoveAnchor)
        cursor.setPosition(hi + 1, QTextCursor.KeepAnchor)
        colorFmt = cursor.charFormat()
        colorFmt.setForeground(color)
        cursor.mergeCharFormat(colorFmt)

    def get_indexes(self):
        """
        获取光标前后第一个和最后一个为数字或字母的下标。
        """
        list_str = self.ui.textEdit.toPlainText()
        cursor = self.ui.textEdit.textCursor()
        # anchor数值为最后一次输入在文档的下标+1。
        hi = cursor.anchor()
        lo = hi - 1
        # 将字体恢复为默认值
        if lo < hi and lo >= 0:
            self.flag_format_changed = True
            cursor.setPosition(lo, QTextCursor.MoveAnchor)
            cursor.setPosition(hi, QTextCursor.KeepAnchor)
            cursor.setCharFormat(self.plainFmt)
        # 限制hi不超过最大长度
        if hi >= len(list_str):
            hi = len(list_str) - 1
        # 向后检查
        while True:
            if hi >= len(list_str) - 1 or not list_str[hi].isalnum():
                if hi > 0 and not list_str[hi].isalnum():
                    hi -= 1
                break
            hi += 1
            pass
        # 向前检查
        while True:
            if lo <= 0 or not list_str[lo].isalnum():
                if lo >= 0 and not list_str[lo].isalnum():
                    lo += 1
                break
            lo -= 1
        return lo, hi

    def color_and_paint(self, text, lo, hi):
        # 在这里设定颜色
        color = QColor()
        if (self.keyword_filter.is_in_bits(text[lo:hi + 1])):
            color.setNamedColor(self.color.keyword)
        elif (self.type_filter.is_in_bits(text[lo:hi + 1])):
            color.setNamedColor(self.color.type_)
        # TODO:number
        # TODO:string
        # TODO:function
        # color.setNamedColor("#c8c8c8")  # tst
        self.paint_text(lo, hi, color)  # 默认颜色

    # 槽函数
    @pyqtSlot()
    def on_textEdit_textChanged(self):
        # 若有发生更改，更改后光标必定是在被更改处的前面，anchor数值为最后一次输入在文档的下标+1。
        # 所以只需要对每次文本更改后位置到前面遇见空白符为止的字符串进行检验，若前后无符号，则可直接拿去检验；若后面有左括号：[({，则将括号删去。
        if self.flag_format_changed:
            self.flag_format_changed = False
            return

        self.file_status.set_TextChanged()

        # set windows name
        if not (self.file_status.is_saved or self.file_status.is_saveFlag_setted):
            self.setWindowTitle(self.file_status.filename+'*')
            self.file_status.is_saveFlag_setted = True

        # set font
        if self.file_status.is_openFile:
            text = self.ui.textEdit.toPlainText()
            idx = 0
            for word in text.split():
                idx = text.find(word, idx)
                self.color_and_paint(text, idx, idx + len(word)-1)
                idx += 1
        else:
            [lo, hi] = self.get_indexes()
            text = self.ui.textEdit.toPlainText()
            self.color_and_paint(text, lo, hi)

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
