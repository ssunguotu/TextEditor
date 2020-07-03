# Pyqt制作代码文本编辑器



文本编辑器所需的基本编辑功能可由自带的QTextEdit控件实现，但是对于关键字高亮、查找替换文本这种操作还需要自己实现。



## 关键字高亮

思路很简单，就是读取字符串进行检索，检查某个字符串段是否在某个布隆过滤器中，若在则令该关键字变色。



### 布隆过滤器



### 令某特定字符串改变颜色

实现思路一般有两种：使用HTML令其变色、使用QT自身的方法改变。

由于改变HTML需要改变文本自身内容，就触发了我所设定的改变颜色检查的signal，方便起见还是使用QT的方法比较好。



具体思路：1. 检索出来某个字符串需要改变颜色  2. 写一个函数，输入为字符串及改变的颜色，操作为将textEdit中该字符串的颜色改变为特定颜色。

#### QTextCursor

> When we refer to "current character" we mean the character immediately *before* the cursor [position](https://doc.qt.io/qt-5/qtextcursor.html#position)() in the document. 

textCursor所代表的就是我们编辑器中的“竖道儿”光标。可以将其理解成一个指针，而每个光标所指向目标就是光标前面的元素。



对于改变某段内容的颜色，第一步是选中这段内容。
QTextEdit的find提供输入字符串就直接选中字符串内容的方法，但是所给的三种查找选项都不符合我们的用法。



**1.选中内容**

pyqt库里面所有类都是只有方法...没有属性。

使用textCursor选中内容，第一步是确定下标区间。

MoveAnchor：将光标移动到的位置，即标志区间的开始。

KeepAnchor：标志区间的结束。

```python
textCursor = self.textEdit.textCursor()#获得光标对象
textCursor.setPosition(3, QTextCursor.MoveAnchor)
textCursor.setPosition(9, QTextCursor.KeepAnchor)
print(textCursor.selectedText())#检验获取内容是否正确
```

这样便完成了内容的选定，选定区间为[3, 9]（对于整个文档而言）。

