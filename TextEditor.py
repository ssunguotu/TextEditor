# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import (QMainWindow, QApplication)
from PyQt5.QtGui import (
    QTextCharFormat,
    QTextCursor,
    QColor,
)
import sys
from Ui_TextEditor import Ui_MainWindow
from bloom_filter import BloomFilter


class TextEditor(QMainWindow, Ui_MainWindow):
    class FontColor():
        keyword = '#AA0D91'
        type_ = '#000080'
        namespace_ = '008080'
        number = '#777777'
        String = '#CD853F'  # 秘鲁棕
        """
        Directive:643820
        keyword:AA0D91
        namespace:008080
        String:C41A16
        """

    ui = Ui_MainWindow()
    formatChanged = False  # 解决无限递归问题
    plainFmt = None  # 解决format错误的问题
    keyword_filter = BloomFilter()
    type_filter = BloomFilter()
    color = FontColor()

    def __init__(self):
        super().__init__()
        self.initUI()  # 界面绘制交给InitUi方法
        self.initFilter()

    def initUI(self):
        self.ui.setupUi(self)
        self.ui.textEdit.setFontPointSize(16)
        self.plainFmt = self.ui.textEdit.currentCharFormat()
        self.ui.textEdit.setStyleSheet("background-color:#F5F5F5")
        self.ui.textBrowser.setStyleSheet("background-color:#F5F5F5")
        self.show()

    def initFilter(self):
        self.keyword_filter.input(['using', 'namespace', 'return'])
        self.type_filter.input(['double', 'int', 'char'])

    def paintText(self, lo, hi, color):
        """
        根据所给的参数在textEdit上对颜色进行修改
        lo：要改变颜色的字符串的开始下标
        hi：结束下标
        color：QColor对象，表示颜色
        """
        if hi <= lo:
            return
        self.formatChanged = True
        cursor = self.ui.textEdit.textCursor()
        cursor.setPosition(lo, QTextCursor.MoveAnchor)
        cursor.setPosition(hi + 1, QTextCursor.KeepAnchor)
        colorFmt = cursor.charFormat()
        colorFmt.setForeground(color)
        cursor.mergeCharFormat(colorFmt)

    def getInxes(self):
        """
        获取光标前后第一个和最后一个为数字或字母的下标。
        """
        strList = self.ui.textEdit.toPlainText()
        cursor = self.ui.textEdit.textCursor()
        # anchor数值为最后一次输入在文档的下标+1。
        hi = cursor.anchor()
        lo = hi - 1
        # 将字体恢复为默认值
        if lo < hi and lo >= 0:
            self.formatChanged = True
            cursor.setPosition(lo, QTextCursor.MoveAnchor)
            cursor.setPosition(hi, QTextCursor.KeepAnchor)
            cursor.setCharFormat(self.plainFmt)
        # 限制hi不超过最大长度
        if hi >= len(strList):
            hi = len(strList) - 1
        # 向后检查
        while True:
            if hi >= len(strList) - 1 or not strList[hi].isalnum():
                if hi > 0 and not strList[hi].isalnum():
                    hi -= 1
                break
            hi += 1
            pass
        # 向前检查
        while True:
            if lo <= 0 or not strList[lo].isalnum():
                if lo >= 0 and not strList[lo].isalnum():
                    lo += 1
                break
            lo -= 1
        return lo, hi

    def colorAndPaint(self, text, lo, hi):
        # 在这里设定颜色
        color = QColor()
        if (self.keyword_filter.isInBits(text[lo:hi + 1])):
            color.setNamedColor(self.color.keyword)
        elif (self.type_filter.isInBits(text[lo:hi + 1])):
            color.setNamedColor(self.color.type_)
        # TODO:number
        # TODO:string
        # TODO:function
        # color.setNamedColor("#c8c8c8")  # tst
        self.paintText(lo, hi, color)  # 默认颜色

    @pyqtSlot()
    def on_textEdit_textChanged(self):
        # 若有发生更改，更改后光标必定是在被更改处的前面，anchor数值为最后一次输入在文档的下标+1。
        # 所以只需要对每次文本更改后位置到前面遇见空白符为止的字符串进行检验，若前后无符号，则可直接拿去检验；若后面有左括号：[({，则将括号删去。
        if self.formatChanged:
            self.formatChanged = False
            return
        [lo, hi] = self.getInxes()
        text = self.ui.textEdit.toPlainText()
        self.colorAndPaint(text, lo, hi)


"""
对于要判断的

tabStopWidth:控制tab的缩进
特别注意：
bug:
    1. 会出现字体变小的情况，在所有字都被删除后。 done
    2. python的非是not！不是～或'！' done
    3. 第一个字母输入的hi应该和lo相等 done
    4. 光标后面的也要判断 done
    5. 
    
"""

if __name__ == '__main__':
    # 创建应用程序和对象
    app = QApplication(sys.argv)
    ex = TextEditor()
    sys.exit(app.exec_())
