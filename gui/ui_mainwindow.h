/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 5.5.0
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QGroupBox>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QProgressBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QStackedWidget>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QWidget *centralWidget;
    QStackedWidget *stackedWidget;
    QWidget *page_3;
    QLabel *label;
    QPushButton *pushButton;
    QWidget *page_5;
    QPushButton *next1;
    QGroupBox *groupBox;
    QLineEdit *filesDir;
    QLineEdit *freecadDir;
    QPushButton *filesDir_push;
    QPushButton *freecadDir_push;
    QLabel *label_2;
    QLabel *label_3;
    QLineEdit *scriptsDir;
    QPushButton *scriptsDir_push;
    QLabel *label_12;
    QLabel *label_4;
    QWidget *page_6;
    QPushButton *next2;
    QGroupBox *groupBox_2;
    QLineEdit *xRodDiaTop;
    QLineEdit *xRodDiaBottom;
    QLineEdit *xRodLength;
    QLabel *label_5;
    QLabel *label_6;
    QLabel *label_7;
    QLabel *label_8;
    QWidget *page_7;
    QPushButton *next3;
    QProgressBar *printerProgress;
    QLabel *label_9;
    QLabel *progressLabel;
    QWidget *page_4;
    QPushButton *quit;
    QLabel *label_10;
    QLabel *label_11;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QStringLiteral("MainWindow"));
        MainWindow->resize(500, 300);
        MainWindow->setMinimumSize(QSize(500, 300));
        MainWindow->setMaximumSize(QSize(500, 300));
        MainWindow->setAnimated(false);
        centralWidget = new QWidget(MainWindow);
        centralWidget->setObjectName(QStringLiteral("centralWidget"));
        stackedWidget = new QStackedWidget(centralWidget);
        stackedWidget->setObjectName(QStringLiteral("stackedWidget"));
        stackedWidget->setGeometry(QRect(0, 0, 501, 301));
        page_3 = new QWidget();
        page_3->setObjectName(QStringLiteral("page_3"));
        label = new QLabel(page_3);
        label->setObjectName(QStringLiteral("label"));
        label->setGeometry(QRect(10, 20, 481, 221));
        label->setPixmap(QPixmap(QString::fromUtf8(":/retr3d.png")));
        label->setScaledContents(true);
        pushButton = new QPushButton(page_3);
        pushButton->setObjectName(QStringLiteral("pushButton"));
        pushButton->setGeometry(QRect(410, 260, 81, 31));
        stackedWidget->addWidget(page_3);
        page_5 = new QWidget();
        page_5->setObjectName(QStringLiteral("page_5"));
        next1 = new QPushButton(page_5);
        next1->setObjectName(QStringLiteral("next1"));
        next1->setEnabled(false);
        next1->setGeometry(QRect(410, 260, 81, 31));
        groupBox = new QGroupBox(page_5);
        groupBox->setObjectName(QStringLiteral("groupBox"));
        groupBox->setGeometry(QRect(30, 60, 441, 181));
        filesDir = new QLineEdit(groupBox);
        filesDir->setObjectName(QStringLiteral("filesDir"));
        filesDir->setGeometry(QRect(20, 40, 321, 20));
        freecadDir = new QLineEdit(groupBox);
        freecadDir->setObjectName(QStringLiteral("freecadDir"));
        freecadDir->setGeometry(QRect(20, 90, 321, 20));
        filesDir_push = new QPushButton(groupBox);
        filesDir_push->setObjectName(QStringLiteral("filesDir_push"));
        filesDir_push->setGeometry(QRect(350, 40, 75, 23));
        freecadDir_push = new QPushButton(groupBox);
        freecadDir_push->setObjectName(QStringLiteral("freecadDir_push"));
        freecadDir_push->setGeometry(QRect(350, 90, 75, 23));
        label_2 = new QLabel(groupBox);
        label_2->setObjectName(QStringLiteral("label_2"));
        label_2->setGeometry(QRect(20, 70, 151, 16));
        label_3 = new QLabel(groupBox);
        label_3->setObjectName(QStringLiteral("label_3"));
        label_3->setGeometry(QRect(20, 20, 151, 16));
        scriptsDir = new QLineEdit(groupBox);
        scriptsDir->setObjectName(QStringLiteral("scriptsDir"));
        scriptsDir->setGeometry(QRect(20, 140, 321, 20));
        scriptsDir_push = new QPushButton(groupBox);
        scriptsDir_push->setObjectName(QStringLiteral("scriptsDir_push"));
        scriptsDir_push->setGeometry(QRect(350, 140, 75, 23));
        label_12 = new QLabel(groupBox);
        label_12->setObjectName(QStringLiteral("label_12"));
        label_12->setGeometry(QRect(20, 120, 151, 16));
        label_4 = new QLabel(page_5);
        label_4->setObjectName(QStringLiteral("label_4"));
        label_4->setGeometry(QRect(20, 20, 461, 31));
        stackedWidget->addWidget(page_5);
        page_6 = new QWidget();
        page_6->setObjectName(QStringLiteral("page_6"));
        next2 = new QPushButton(page_6);
        next2->setObjectName(QStringLiteral("next2"));
        next2->setEnabled(true);
        next2->setGeometry(QRect(410, 260, 81, 31));
        groupBox_2 = new QGroupBox(page_6);
        groupBox_2->setObjectName(QStringLiteral("groupBox_2"));
        groupBox_2->setGeometry(QRect(10, 60, 301, 181));
        xRodDiaTop = new QLineEdit(groupBox_2);
        xRodDiaTop->setObjectName(QStringLiteral("xRodDiaTop"));
        xRodDiaTop->setGeometry(QRect(150, 30, 131, 20));
        xRodDiaBottom = new QLineEdit(groupBox_2);
        xRodDiaBottom->setObjectName(QStringLiteral("xRodDiaBottom"));
        xRodDiaBottom->setGeometry(QRect(150, 80, 131, 20));
        xRodLength = new QLineEdit(groupBox_2);
        xRodLength->setObjectName(QStringLiteral("xRodLength"));
        xRodLength->setGeometry(QRect(150, 130, 131, 20));
        label_5 = new QLabel(groupBox_2);
        label_5->setObjectName(QStringLiteral("label_5"));
        label_5->setGeometry(QRect(10, 30, 131, 16));
        label_6 = new QLabel(groupBox_2);
        label_6->setObjectName(QStringLiteral("label_6"));
        label_6->setGeometry(QRect(10, 80, 131, 16));
        label_7 = new QLabel(groupBox_2);
        label_7->setObjectName(QStringLiteral("label_7"));
        label_7->setGeometry(QRect(10, 130, 131, 16));
        label_8 = new QLabel(page_6);
        label_8->setObjectName(QStringLiteral("label_8"));
        label_8->setGeometry(QRect(320, 20, 171, 221));
        label_8->setPixmap(QPixmap(QString::fromUtf8(":/xRod.png")));
        label_8->setScaledContents(true);
        stackedWidget->addWidget(page_6);
        page_7 = new QWidget();
        page_7->setObjectName(QStringLiteral("page_7"));
        next3 = new QPushButton(page_7);
        next3->setObjectName(QStringLiteral("next3"));
        next3->setEnabled(false);
        next3->setGeometry(QRect(410, 260, 81, 31));
        printerProgress = new QProgressBar(page_7);
        printerProgress->setObjectName(QStringLiteral("printerProgress"));
        printerProgress->setGeometry(QRect(50, 70, 411, 23));
        printerProgress->setValue(0);
        label_9 = new QLabel(page_7);
        label_9->setObjectName(QStringLiteral("label_9"));
        label_9->setGeometry(QRect(50, 50, 111, 16));
        progressLabel = new QLabel(page_7);
        progressLabel->setObjectName(QStringLiteral("progressLabel"));
        progressLabel->setGeometry(QRect(50, 100, 381, 16));
        stackedWidget->addWidget(page_7);
        page_4 = new QWidget();
        page_4->setObjectName(QStringLiteral("page_4"));
        quit = new QPushButton(page_4);
        quit->setObjectName(QStringLiteral("quit"));
        quit->setGeometry(QRect(410, 260, 81, 31));
        label_10 = new QLabel(page_4);
        label_10->setObjectName(QStringLiteral("label_10"));
        label_10->setGeometry(QRect(10, 20, 361, 201));
        label_11 = new QLabel(page_4);
        label_11->setObjectName(QStringLiteral("label_11"));
        label_11->setGeometry(QRect(370, 20, 141, 61));
        label_11->setPixmap(QPixmap(QString::fromUtf8(":/gpl.png")));
        stackedWidget->addWidget(page_4);
        MainWindow->setCentralWidget(centralWidget);

        retranslateUi(MainWindow);

        stackedWidget->setCurrentIndex(0);


        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QApplication::translate("MainWindow", "Retr3d", 0));
        label->setText(QString());
        pushButton->setText(QApplication::translate("MainWindow", "Begin", 0));
        next1->setText(QApplication::translate("MainWindow", "Next", 0));
        groupBox->setTitle(QApplication::translate("MainWindow", "Locations", 0));
        freecadDir->setText(QApplication::translate("MainWindow", "C:/Program Files (x86)/FreeCAD 0.15/bin", 0));
        filesDir_push->setText(QApplication::translate("MainWindow", "Browse...", 0));
        freecadDir_push->setText(QApplication::translate("MainWindow", "Browse...", 0));
        label_2->setText(QApplication::translate("MainWindow", "Where FreeCAD is Located", 0));
        label_3->setText(QApplication::translate("MainWindow", "Where to Store Printer Files", 0));
        scriptsDir->setText(QString());
        scriptsDir_push->setText(QApplication::translate("MainWindow", "Browse...", 0));
        label_12->setText(QApplication::translate("MainWindow", "Location of Retr3d Scripts", 0));
        label_4->setText(QApplication::translate("MainWindow", "Retr3d needs to know where things are. Please take a moment and input some file paths.", 0));
        next2->setText(QApplication::translate("MainWindow", "Next", 0));
        groupBox_2->setTitle(QApplication::translate("MainWindow", "X Rod", 0));
        xRodDiaTop->setText(QApplication::translate("MainWindow", "7.9", 0));
        xRodDiaBottom->setText(QApplication::translate("MainWindow", "7.9", 0));
        xRodLength->setText(QApplication::translate("MainWindow", "400", 0));
        label_5->setText(QApplication::translate("MainWindow", "Top X Rod Diameter", 0));
        label_6->setText(QApplication::translate("MainWindow", "Bottom X Rod Diameter", 0));
        label_7->setText(QApplication::translate("MainWindow", "Length of the Shorter Rod", 0));
        label_8->setText(QString());
        next3->setText(QApplication::translate("MainWindow", "Next", 0));
        label_9->setText(QApplication::translate("MainWindow", "Building Printer Files", 0));
        progressLabel->setText(QString());
        quit->setText(QApplication::translate("MainWindow", "Finish", 0));
        label_10->setText(QApplication::translate("MainWindow", "This file is part of Retr3d.\n"
"\n"
"Retr3d is free software: you can redistribute it and/or modify\n"
"it under the terms of the GNU General Public License as published by\n"
"the Free Software Foundation, either version 3 of the License, or\n"
"(at your option) any later version.\n"
"\n"
"Retr3d is distributed in the hope that it will be useful,\n"
"but WITHOUT ANY WARRANTY; without even the implied warranty of\n"
"MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n"
"GNU General Public License for more details.\n"
"\n"
"You should have received a copy of the GNU General Public License\n"
"along with Retr3d.  If not, see <http://www.gnu.org/licenses/>.", 0));
        label_11->setText(QString());
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
