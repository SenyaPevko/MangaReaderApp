# Form implementation generated from reading ui file '.\settings_widget_preview.ui'
#
# Created by: PyQt6 UI code generator 6.5.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_settingsWidget(object):
    def setupUi(self, settingsWidget):
        settingsWidget.setObjectName("settingsWidget")
        settingsWidget.resize(400, 127)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(settingsWidget.sizePolicy().hasHeightForWidth())
        settingsWidget.setSizePolicy(sizePolicy)
        settingsWidget.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(settingsWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widgetFrame = QtWidgets.QFrame(parent=settingsWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widgetFrame.sizePolicy().hasHeightForWidth())
        self.widgetFrame.setSizePolicy(sizePolicy)
        self.widgetFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.widgetFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.widgetFrame.setObjectName("widgetFrame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widgetFrame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.icon = QtWidgets.QLabel(parent=self.widgetFrame)
        self.icon.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        self.icon.setObjectName("icon")
        self.horizontalLayout.addWidget(self.icon)
        self.textFrame = QtWidgets.QFrame(parent=self.widgetFrame)
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
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.verticalLayout.addItem(spacerItem1)
        self.titleLabel = QtWidgets.QLabel(parent=self.textFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titleLabel.sizePolicy().hasHeightForWidth())
        self.titleLabel.setSizePolicy(sizePolicy)
        self.titleLabel.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.titleLabel.setObjectName("titleLabel")
        self.verticalLayout.addWidget(self.titleLabel)
        self.descriptionLabel = QtWidgets.QLabel(parent=self.textFrame)
        self.descriptionLabel.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.descriptionLabel.setObjectName("descriptionLabel")
        self.verticalLayout.addWidget(self.descriptionLabel)
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.verticalLayout.addItem(spacerItem2)
        self.horizontalLayout.addWidget(self.textFrame)
        self.verticalLayout_2.addWidget(self.widgetFrame)

        self.retranslateUi(settingsWidget)
        QtCore.QMetaObject.connectSlotsByName(settingsWidget)

    def retranslateUi(self, settingsWidget):
        _translate = QtCore.QCoreApplication.translate
        settingsWidget.setWindowTitle(_translate("settingsWidget", "Form"))
        self.icon.setText(_translate("settingsWidget", "TextLabel"))
        self.titleLabel.setText(_translate("settingsWidget", "TextLabel"))
        self.descriptionLabel.setText(_translate("settingsWidget", "TextLabel"))