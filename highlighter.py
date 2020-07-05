from bloom_filter import BloomFilter
from PyQt5.QtWidgets import (QMainWindow, QApplication, QFileDialog)
from PyQt5.QtGui import (
    QTextCharFormat,
    QTextCursor,
    QColor,
)

class Highlighter(object):
    class FontColor():
        keyword = '#AA0D91'
        type_ = '#4169E1'
        namespace_ = '008080'
        number = '#777777'
        String = '#CD853F'  # 秘鲁棕

    def __init__(self, ui):
        self.ui = ui
        self.precompile_filter = BloomFilter()
        self.keyword_filter = BloomFilter(7, 10000)
        self.plainFmt = None # 解决format错误的问题
        self.flag_format_changed = False  # 解决无限递归问题
        self.init_filter()
        self.color = self.FontColor()
        self.plainFmt = self.ui.textEdit.currentCharFormat()

    def init_filter(self):
        with open('precompile.txt', 'r', encoding='UTF-8') as f:
            compileword = [li.split()[0] for li in f.readlines()]
        self.precompile_filter.input(compileword)
        with open('keyword.txt', 'r', encoding='UTF-8') as f:
            allword = [li.split()[0] for li in f.readlines()]
        self.keyword_filter.input(allword)

    def mode_normal(self):
        # 若有发生更改，更改后光标必定是在被更改处的前面，anchor数值为最后一次输入在文档的下标+1。
        # 所以只需要对每次文本更改后位置到前面遇见空白符为止的字符串进行检验，若前后无符号，则可直接拿去检验；若后面有左括号：[({，则将括号删去。
        [lo, hi] = self.get_indexes()
        text = self.ui.textEdit.toPlainText()
        self.color_and_paint(text, lo, hi)

    def mode_openfile(self):
        def is_right(s):
            if s.isalnum() or s in '#_':  # 字母或数字
                return True
            return False

        text = self.ui.textEdit.toPlainText()
        lo, hi = 0, 0
        while hi < len(text):
            if is_right(text[lo]):
                while hi < len(text) and is_right(text[hi]):
                    hi += 1
                self.color_and_paint(text, lo, hi-1)
                lo = hi
            else:
                lo, hi = lo+1, hi+1

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
        if (self.precompile_filter.is_in_bits(text[lo:hi + 1])):
            color.setNamedColor(self.color.keyword)
        elif (self.keyword_filter.is_in_bits(text[lo:hi + 1])):
            color.setNamedColor(self.color.type_)
        # TODO:number
        # TODO:string
        # TODO:function
        # color.setNamedColor("#c8c8c8")  # tst
        self.paint_text(lo, hi, color)  # 默认颜色
