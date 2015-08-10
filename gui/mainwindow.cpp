#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "makeprinter.h"
#include <Python.h>
#include "QFileDialog"
#include <iostream>
#include <thread>
#include "QThread"
#include "QFuture"
#include "QtConcurrent/QtConcurrent"
using namespace std;

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_pushButton_clicked()
{
    ui->stackedWidget->setCurrentIndex(1);
}

void MainWindow::on_next1_clicked()
{
    ui->stackedWidget->setCurrentIndex(2);
    QFuture<void> t1 = QtConcurrent::run(foo);
}

void MainWindow::on_next2_clicked()
{
    ui->stackedWidget->setCurrentIndex(3);
    Py_Initialize();
    ui->printerProgress->setValue(0);
    PyRun_SimpleString("import sys");
    size_t index = 0;
    std::string str;
    str = ((ui->freecadDir->text()).toStdString());
    while (true) {
         /* Locate the substring to replace. */
         index = str.find("/", index);
         if (index == std::string::npos) break;

         /* Make the replacement. */
         str.replace(index, 1, "\\\\");

         /* Advance index forward so the next iteration doesn't pick it up as well. */
         index += 3;
    }
    str = str+"\\\\";
QString label = "loading...";
ui->progressLabel->setText(label);
ui->printerProgress->setValue(10);



    Py_Finalize();
}


void MainWindow::on_next3_clicked()
{
    ui->stackedWidget->setCurrentIndex(4);
}

void MainWindow::on_quit_clicked()
{
    close();
}

void MainWindow::on_filesDir_push_clicked()
{
    QString dir = QFileDialog::getExistingDirectory(this, tr("Open Directory"),
                                                 "/home",
                                                 QFileDialog::ShowDirsOnly
                                                 | QFileDialog::DontResolveSymlinks);
    ui->filesDir->setText(dir);
}

void MainWindow::on_freecadDir_push_clicked()
{
    QString dir = QFileDialog::getExistingDirectory(this, tr("Open Directory"),
                                                 "/home",
                                                 QFileDialog::ShowDirsOnly
                                                 | QFileDialog::DontResolveSymlinks);
    ui->freecadDir->setText(dir);
}

