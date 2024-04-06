# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chatboxUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1076, 698)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setStyleSheet("#frame{\n"
"    \n"
"    background-image: url(./designer/2.png);\n"
"}")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.listWidget = QtWidgets.QListWidget(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy)
        self.listWidget.setStyleSheet("QListWidget {\n"
"    font: 13pt \"Cooper Black\";\n"
"    background-color:qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0.0597015 rgba(22, 14, 116, 255), stop:0.507463 rgba(19, 11, 99, 255), stop:0.925373 rgba(0, 0, 0, 255));\n"
"    border: none;\n"
"}\n"
"\n"
"QListWidget::item {\n"
"    color: white;  \n"
"}\n"
"\n"
"QListWidget::item:selected {\n"
"    background-color:rgb(29, 28, 28);\n"
"    border: 1px solid white; \n"
"    border-radius: 22px;\n"
"\n"
"}\n"
"\n"
"QListWidget::item:hover { \n"
"    color: rgb(61, 56, 55);\n"
"}\n"
"\n"
"QListView::item {\n"
"    height: 50px;\n"
"    border: 1px solid white; \n"
"    border-radius: 22px;\n"
"}")
        self.listWidget.setObjectName("listWidget")
        self.horizontalLayout_2.addWidget(self.listWidget)
        self.widget = QtWidgets.QWidget(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(8)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_2 = QtWidgets.QWidget(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.widget_2.setStyleSheet("QPushButton{\n"
"    background-color:rgb(20, 20, 20);\n"
"    border:none;\n"
"    border-radius:15px;\n"
"}\n"
"QToolButton{\n"
"    background-color:rgb(20, 20, 20);\n"
"    border:none;\n"
"    border-radius:15px;\n"
"}")
        self.widget_2.setObjectName("widget_2")
        self.pushButton_5 = QtWidgets.QPushButton(self.widget_2)
        self.pushButton_5.setGeometry(QtCore.QRect(730, 0, 81, 40))
        self.pushButton_5.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_5.setStyleSheet("")
        self.pushButton_5.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("designer/video-solid.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_5.setIcon(icon)
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(self.widget_2)
        self.pushButton_6.setGeometry(QtCore.QRect(550, 0, 81, 40))
        self.pushButton_6.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_6.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("designer/record-vinyl-solid-white.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_6.setIcon(icon1)
        self.pushButton_6.setObjectName("pushButton_6")
        self.toolButton = QtWidgets.QToolButton(self.widget_2)
        self.toolButton.setGeometry(QtCore.QRect(640, 0, 81, 41))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("designer/wand-magic-sparkles-solid.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton.setIcon(icon2)
        self.toolButton.setObjectName("toolButton")
        self.verticalLayout.addWidget(self.widget_2)
        self.widget_4 = QtWidgets.QWidget(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(8)
        sizePolicy.setVerticalStretch(22)
        sizePolicy.setHeightForWidth(self.widget_4.sizePolicy().hasHeightForWidth())
        self.widget_4.setSizePolicy(sizePolicy)
        self.widget_4.setObjectName("widget_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget_4)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.textEdit = QtWidgets.QTextEdit(self.widget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        self.textEdit.setMinimumSize(QtCore.QSize(395, 498))
        self.textEdit.setObjectName("textEdit")
        self.horizontalLayout_3.addWidget(self.textEdit)
        self.label = QtWidgets.QLabel(self.widget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(394, 498))
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.verticalLayout.addWidget(self.widget_4)
        self.widget_3 = QtWidgets.QWidget(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy)
        self.widget_3.setStyleSheet("")
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget_3)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.pushButton_3 = QtWidgets.QPushButton(self.widget_3)
        self.pushButton_3.setMinimumSize(QtCore.QSize(38, 38))
        self.pushButton_3.setMaximumSize(QtCore.QSize(38, 38))
        self.pushButton_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_3.setStyleSheet("#pushButton_3{\n"
"    background-color:rgb(20, 20, 20);\n"
"    border:none;\n"
"    border-radius:15px;\n"
"}")
        self.pushButton_3.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("designer/microphone-solid.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_3.setIcon(icon3)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_4.addWidget(self.pushButton_3)
        self.pushButton = QtWidgets.QPushButton(self.widget_3)
        self.pushButton.setMinimumSize(QtCore.QSize(38, 38))
        self.pushButton.setMaximumSize(QtCore.QSize(38, 38))
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton.setStyleSheet("#pushButton{\n"
"    background-color:rgb(20, 20, 20);\n"
"    border:none;\n"
"    border-radius:15px;\n"
"}")
        self.pushButton.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("designer/volume-high-solid-white.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon4)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_4.addWidget(self.pushButton)
        self.textEdit_2 = QtWidgets.QTextEdit(self.widget_3)
        self.textEdit_2.setMaximumSize(QtCore.QSize(600, 35))
        self.textEdit_2.setObjectName("textEdit_2")
        self.horizontalLayout_4.addWidget(self.textEdit_2)
        self.pushButton_2 = QtWidgets.QPushButton(self.widget_3)
        self.pushButton_2.setMinimumSize(QtCore.QSize(70, 38))
        self.pushButton_2.setMaximumSize(QtCore.QSize(70, 38))
        self.pushButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_2.setStyleSheet("#pushButton_2{\n"
"    background-color:rgb(20, 20, 20);\n"
"    border:none;\n"
"    border-radius:15px;\n"
"}")
        self.pushButton_2.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("designer/paper-plane-solid.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon5)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_4.addWidget(self.pushButton_2)
        self.verticalLayout.addWidget(self.widget_3)
        self.horizontalLayout_2.addWidget(self.widget)
        self.horizontalLayout.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.toolButton.setText(_translate("MainWindow", "..."))
        self.label.setText(_translate("MainWindow", "TextLabel"))
