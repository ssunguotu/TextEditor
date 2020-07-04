# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\dell\Desktop\TextEditor\text_editor.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(805, 605)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(40, 0, 761, 561))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.textEdit.setFont(font)
        self.textEdit.setTabStopWidth(20)
        self.textEdit.setObjectName("textEdit")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(0, 0, 41, 561))
        self.textBrowser.setObjectName("textBrowser")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 805, 26))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtWidgets.QMenu(self.menubar)
        self.menu_3.setObjectName("menu_3")
        self.menu_4 = QtWidgets.QMenu(self.menubar)
        self.menu_4.setObjectName("menu_4")
        self.menu_5 = QtWidgets.QMenu(self.menubar)
        self.menu_5.setObjectName("menu_5")
        self.menubloomFilter = QtWidgets.QMenu(self.menubar)
        self.menubloomFilter.setObjectName("menubloomFilter")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.act_new = QtWidgets.QAction(MainWindow)
        self.act_new.setObjectName("act_new")
        self.act_open = QtWidgets.QAction(MainWindow)
        self.act_open.setObjectName("act_open")
        self.act_saveAs = QtWidgets.QAction(MainWindow)
        self.act_saveAs.setObjectName("act_saveAs")
        self.act_save = QtWidgets.QAction(MainWindow)
        self.act_save.setObjectName("act_save")
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.action_2 = QtWidgets.QAction(MainWindow)
        self.action_2.setObjectName("action_2")
        self.action_3 = QtWidgets.QAction(MainWindow)
        self.action_3.setObjectName("action_3")
        self.action_4 = QtWidgets.QAction(MainWindow)
        self.action_4.setObjectName("action_4")
        self.actionC = QtWidgets.QAction(MainWindow)
        self.actionC.setObjectName("actionC")
        self.menu_File.addAction(self.act_new)
        self.menu_File.addAction(self.act_open)
        self.menu_File.addAction(self.act_saveAs)
        self.menu_File.addAction(self.act_save)
        self.menu_2.addAction(self.action_2)
        self.menu_2.addSeparator()
        self.menu_2.addAction(self.action)
        self.menu_2.addAction(self.action_3)
        self.menu_2.addAction(self.action_4)
        self.menubloomFilter.addAction(self.actionC)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.menu_4.menuAction())
        self.menubar.addAction(self.menu_5.menuAction())
        self.menubar.addAction(self.menubloomFilter.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.textEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:16pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Ubuntu\';\"><br /></p></body></html>"))
        self.menu_File.setTitle(_translate("MainWindow", "文件"))
        self.menu_2.setTitle(_translate("MainWindow", "编辑"))
        self.menu_3.setTitle(_translate("MainWindow", "格式"))
        self.menu_4.setTitle(_translate("MainWindow", "查看"))
        self.menu_5.setTitle(_translate("MainWindow", "帮助"))
        self.menubloomFilter.setTitle(_translate("MainWindow", "bloomFilter"))
        self.act_new.setText(_translate("MainWindow", "新建"))
        self.act_new.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.act_open.setText(_translate("MainWindow", "打开..."))
        self.act_open.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.act_saveAs.setText(_translate("MainWindow", "另存为"))
        self.act_saveAs.setShortcut(_translate("MainWindow", "Ctrl+Shift+S"))
        self.act_save.setText(_translate("MainWindow", "保存"))
        self.act_save.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.action.setText(_translate("MainWindow", "剪切"))
        self.action_2.setText(_translate("MainWindow", "撤销"))
        self.action_3.setText(_translate("MainWindow", "复制"))
        self.action_4.setText(_translate("MainWindow", "粘贴"))
        self.actionC.setText(_translate("MainWindow", "添加新词"))
