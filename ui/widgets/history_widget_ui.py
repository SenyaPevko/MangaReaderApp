# Form implementation generated from reading ui file '.\history_widget.ui'
#
# Created by: PyQt6 UI code generator 6.5.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets

from utils.clickable_label import ClickableLabel


class Ui_historyWidget(object):
    def setupUi(self, historyWidget):
        historyWidget.setObjectName("historyWidget")
        historyWidget.resize(400, 152)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(historyWidget.sizePolicy().hasHeightForWidth())
        historyWidget.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(historyWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.historyFrame = QtWidgets.QFrame(parent=historyWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.historyFrame.sizePolicy().hasHeightForWidth())
        self.historyFrame.setSizePolicy(sizePolicy)
        self.historyFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.historyFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.historyFrame.setObjectName("historyFrame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.historyFrame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.image = ClickableLabel(parent=self.historyFrame)
        self.image.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.image.setObjectName("image")
        self.horizontalLayout.addWidget(self.image)
        self.textFrame = QtWidgets.QFrame(parent=self.historyFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textFrame.sizePolicy().hasHeightForWidth())
        self.textFrame.setSizePolicy(sizePolicy)
        self.textFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.textFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.textFrame.setObjectName("textFrame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.textFrame)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(20, 30, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.verticalLayout.addItem(spacerItem1)
        self.mangaNameLabel = ClickableLabel(parent=self.textFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mangaNameLabel.sizePolicy().hasHeightForWidth())
        self.mangaNameLabel.setSizePolicy(sizePolicy)
        self.mangaNameLabel.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.mangaNameLabel.setObjectName("mangaNameLabel")
        self.verticalLayout.addWidget(self.mangaNameLabel)
        self.mangaHistoryLabel = ClickableLabel(parent=self.textFrame)
        self.mangaHistoryLabel.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.mangaHistoryLabel.setObjectName("mangaHistoryLabel")
        self.verticalLayout.addWidget(self.mangaHistoryLabel)
        spacerItem2 = QtWidgets.QSpacerItem(20, 30, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.verticalLayout.addItem(spacerItem2)
        self.horizontalLayout.addWidget(self.textFrame)
        self.deleteButton = ClickableLabel(parent=self.historyFrame)
        self.deleteButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.deleteButton.setObjectName("deleteButton")
        self.horizontalLayout.addWidget(self.deleteButton)
        spacerItem3 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.verticalLayout_2.addWidget(self.historyFrame)

        self.retranslateUi(historyWidget)
        QtCore.QMetaObject.connectSlotsByName(historyWidget)

    def retranslateUi(self, historyWidget):
        _translate = QtCore.QCoreApplication.translate
        historyWidget.setWindowTitle(_translate("historyWidget", "Form"))
        self.image.setText(_translate("historyWidget", "TextLabel"))
        self.mangaNameLabel.setText(_translate("historyWidget", "TextLabel"))
        self.mangaHistoryLabel.setText(_translate("historyWidget", "TextLabel"))
        self.deleteButton.setText(_translate("historyWidget", "TextLabel"))
