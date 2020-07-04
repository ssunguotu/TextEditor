from bloom_filter import BloomFilter
from font_config import FontColor
from PyQt5.QtWidgets import (QMainWindow, QApplication, QFileDialog)
from PyQt5.QtGui import (
    QTextCharFormat,
    QTextCursor,
    QColor,
)

class Highlighter(object):
    def __init__(self, ui):
        self.ui = ui
        self.keyword_filter = BloomFilter()
        self.type_filter = BloomFilter()
        self.plainFmt = None # 解决format错误的问题
        self.flag_format_changed = False  # 解决无限递归问题
        self.init_filter()
        self.color = FontColor()
        self.plainFmt = self.ui.textEdit.currentCharFormat()


    def init_filter(self):
        with open('cpp.txt', 'r') as f:
            allword = [li.split()[0] for li in f.readlines()]
        self.keyword_filter.input(allword)
        # self.keyword_filter.input(['using', 'namespace', 'return'])
        self.type_filter.input(['double', 'int', 'char'])

    def mode_normal(self):
        [lo, hi] = self.get_indexes()
        text = self.ui.textEdit.toPlainText()
        self.color_and_paint(text, lo, hi)

    def mode_openfile(self):
        text = self.ui.textEdit.toPlainText()
        idx = 0
        for word in text.split():
            idx = text.find(word, idx)
            self.color_and_paint(text, idx, idx + len(word)-1)
            idx += 1

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
