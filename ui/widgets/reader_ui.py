# Form implementation generated from reading ui file '.\reader.ui'
#
# Created by: PyQt6 UI code generator 6.5.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(688, 721)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.imagesFrame = QtWidgets.QFrame(parent=Form)
        self.imagesFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.imagesFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.imagesFrame.setObjectName("imagesFrame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.imagesFrame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.imagesScrollArea = QtWidgets.QScrollArea(parent=self.imagesFrame)
        self.imagesScrollArea.setWidgetResizable(True)
        self.imagesScrollArea.setObjectName("imagesScrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 648, 631))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.imageLabel = QtWidgets.QLabel(parent=self.scrollAreaWidgetContents)
        self.imageLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter|QtCore.Qt.AlignmentFlag.AlignTop)
        self.imageLabel.setObjectName("imageLabel")
        self.verticalLayout_2.addWidget(self.imageLabel)
        self.imagesScrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout_2.addWidget(self.imagesScrollArea)
        self.verticalLayout.addWidget(self.imagesFrame)
        self.buttonsFrame = QtWidgets.QFrame(parent=Form)
        self.buttonsFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.buttonsFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.buttonsFrame.setObjectName("buttonsFrame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.buttonsFrame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.exitButton = QtWidgets.QPushButton(parent=self.buttonsFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exitButton.sizePolicy().hasHeightForWidth())
        self.exitButton.setSizePolicy(sizePolicy)
        self.exitButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.exitButton.setAutoRepeatDelay(299)
        self.exitButton.setObjectName("exitButton")
        self.horizontalLayout.addWidget(self.exitButton)
        self.previousPageButton = QtWidgets.QPushButton(parent=self.buttonsFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.previousPageButton.sizePolicy().hasHeightForWidth())
        self.previousPageButton.setSizePolicy(sizePolicy)
        self.previousPageButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.previousPageButton.setAutoRepeatDelay(299)
        self.previousPageButton.setObjectName("previousPageButton")
        self.horizontalLayout.addWidget(self.previousPageButton)
        self.chaptersList = QtWidgets.QComboBox(parent=self.buttonsFrame)
        self.chaptersList.setObjectName("chaptersList")
        self.horizontalLayout.addWidget(self.chaptersList)
        self.pagesLabel = QtWidgets.QLabel(parent=self.buttonsFrame)
        self.pagesLabel.setObjectName("pagesLabel")
        self.horizontalLayout.addWidget(self.pagesLabel)
        self.nextPageButton = QtWidgets.QPushButton(parent=self.buttonsFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nextPageButton.sizePolicy().hasHeightForWidth())
        self.nextPageButton.setSizePolicy(sizePolicy)
        self.nextPageButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.nextPageButton.setAutoRepeatDelay(299)
        self.nextPageButton.setObjectName("nextPageButton")
        self.horizontalLayout.addWidget(self.nextPageButton)
        self.verticalLayout.addWidget(self.buttonsFrame)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.imageLabel.setText(_translate("Form", "Image"))
        self.exitButton.setText(_translate("Form", "Выйти"))
        self.exitButton.setShortcut(_translate("Form", "Esc"))
        self.previousPageButton.setText(_translate("Form", "Назад"))
        self.previousPageButton.setShortcut(_translate("Form", "Left"))
        self.pagesLabel.setText(_translate("Form", "Страница 1"))
        self.nextPageButton.setText(_translate("Form", "Вперед"))
        self.nextPageButton.setShortcut(_translate("Form", "Right"))
