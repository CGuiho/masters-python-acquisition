# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'designuiBLGrRT.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGraphicsView, QLabel, QMainWindow,
    QMenuBar, QPushButton, QScrollArea, QSizePolicy,
    QStatusBar, QTextBrowser, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1219, 911)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setGeometry(QRect(0, 130, 1201, 711))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1199, 709))
        self.stats_main = QLabel(self.scrollAreaWidgetContents)
        self.stats_main.setObjectName(u"stats_main")
        self.stats_main.setGeometry(QRect(100, 40, 111, 51))
        self.stats_main_label = QLabel(self.scrollAreaWidgetContents)
        self.stats_main_label.setObjectName(u"stats_main_label")
        self.stats_main_label.setGeometry(QRect(30, 40, 61, 51))
        self.stats_std_label = QLabel(self.scrollAreaWidgetContents)
        self.stats_std_label.setObjectName(u"stats_std_label")
        self.stats_std_label.setGeometry(QRect(240, 40, 61, 51))
        self.stats_std = QLabel(self.scrollAreaWidgetContents)
        self.stats_std.setObjectName(u"stats_std")
        self.stats_std.setGeometry(QRect(310, 40, 111, 51))
        self.stats_variance_label = QLabel(self.scrollAreaWidgetContents)
        self.stats_variance_label.setObjectName(u"stats_variance_label")
        self.stats_variance_label.setGeometry(QRect(240, 110, 61, 51))
        self.stats_variance = QLabel(self.scrollAreaWidgetContents)
        self.stats_variance.setObjectName(u"stats_variance")
        self.stats_variance.setGeometry(QRect(310, 110, 111, 51))
        self.stats_max_label = QLabel(self.scrollAreaWidgetContents)
        self.stats_max_label.setObjectName(u"stats_max_label")
        self.stats_max_label.setGeometry(QRect(450, 40, 61, 51))
        self.stats_max = QLabel(self.scrollAreaWidgetContents)
        self.stats_max.setObjectName(u"stats_max")
        self.stats_max.setGeometry(QRect(520, 40, 111, 51))
        self.stats_min = QLabel(self.scrollAreaWidgetContents)
        self.stats_min.setObjectName(u"stats_min")
        self.stats_min.setGeometry(QRect(520, 110, 111, 51))
        self.stats_min_label = QLabel(self.scrollAreaWidgetContents)
        self.stats_min_label.setObjectName(u"stats_min_label")
        self.stats_min_label.setGeometry(QRect(450, 110, 61, 51))
        self.graphicsView = QGraphicsView(self.scrollAreaWidgetContents)
        self.graphicsView.setObjectName(u"graphicsView")
        self.graphicsView.setGeometry(QRect(30, 210, 1131, 301))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.textBrowser = QTextBrowser(self.centralwidget)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setGeometry(QRect(60, 10, 431, 121))
        self.fetch_data = QPushButton(self.centralwidget)
        self.fetch_data.setObjectName(u"fetch_data")
        self.fetch_data.setGeometry(QRect(530, 30, 201, 71))
        self.save_csv = QPushButton(self.centralwidget)
        self.save_csv.setObjectName(u"save_csv")
        self.save_csv.setGeometry(QRect(760, 30, 201, 71))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1219, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.stats_main.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.stats_main_label.setText(QCoreApplication.translate("MainWindow", u"Moyenne:", None))
        self.stats_std_label.setText(QCoreApplication.translate("MainWindow", u"Ecart Type: ", None))
        self.stats_std.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.stats_variance_label.setText(QCoreApplication.translate("MainWindow", u"Variance:", None))
        self.stats_variance.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.stats_max_label.setText(QCoreApplication.translate("MainWindow", u"Max:", None))
        self.stats_max.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.stats_min.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.stats_min_label.setText(QCoreApplication.translate("MainWindow", u"Min:", None))
        self.textBrowser.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">Crist\u00f3v\u00e3o GUIHO</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">https://guiho.co</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-siz"
                        "e:14pt;\">M2 3EA T3I </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">Programmation et Acquisition</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:14pt;\"><br /></p></body></html>", None))
        self.fetch_data.setText(QCoreApplication.translate("MainWindow", u"R\u00e9cuperer Les Donn\u00e9es", None))
        self.save_csv.setText(QCoreApplication.translate("MainWindow", u"Sauvegarder en CSV", None))
    # retranslateUi

