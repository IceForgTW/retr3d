#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "makeprinter.h"
#include "worker.h"
#include <Python.h>
#include "QFileDialog"
#include <iostream>
#include <thread>
#include "QThread"
#include "QFuture"
#include "QtConcurrent/QtConcurrent"
#include "QObject"
#include <QDebug>
using namespace std;
int value(5);

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    // The thread and the worker are created in the constructor so it is always safe to delete them.
    thread = new QThread();
    worker = new Worker();

    worker->moveToThread(thread);
    connect(worker, SIGNAL(valueChanged(QString)), SLOT(onProgressChanged(QString)));
    connect(worker, SIGNAL(workRequested()), thread, SLOT(start()));
    connect(thread, SIGNAL(started()), worker, SLOT(doWork()));
    connect(worker, SIGNAL(finished()), thread, SLOT(quit()), Qt::DirectConnection);
}

MainWindow::~MainWindow()
{
    worker->abort();
    thread->wait();
    qDebug()<<"Deleting thread and worker in Thread "<<this->QObject::thread()->currentThreadId();
    delete thread;
    delete worker;

    delete ui;
}

void MainWindow::onProgressChanged(QString info) {
    // Processing code
    ui->printerProgress->setValue(info.toInt());
    ui->progressLabel->setText(status());
}

void MainWindow::on_pushButton_clicked()
{
    ui->stackedWidget->setCurrentIndex(1);
}

void MainWindow::on_next1_clicked()
{
    ui->stackedWidget->setCurrentIndex(2);
    QFuture<void> t1 = QtConcurrent::run(foo);
    // To avoid having two threads running simultaneously, the previous thread is aborted.
    worker->abort();

    //ui->printerProgress->setValue(10);
    thread->wait(); // If the thread is not running, this will immediately return.

    worker->requestWork();
}

void MainWindow::on_next2_clicked()
{
    ui->stackedWidget->setCurrentIndex(3);
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

class GUIUpdater : public QObject {
    Q_OBJECT

public:
    explicit GUIUpdater(QObject *parent = 0) : QObject(parent) {}
    void newLabel(const QString &image) { emit requestNewLabel(image); }

signals:
    void requestNewLabel(const QString &);
};

void MainWindow::updateProgress()
{
    while(true){
    QThread::msleep(200);
    cout << bar() << endl;
    int x;
    x=bar();
    cout << x << endl;
    //ui->printerProgress->setValue(x);


    }
}

void MainWindow::startWorkInAThread() {
    // Create an instance of your woker
    //makePrinter *src = new makePrinter;
    // Connect our signal and slot
    //QObject::connect(src, SIGNAL(progressChanged(int)), SLOT(onProgressChagned(int)));
    // Setup callback for cleanup when it finishes
    //connect(src, SIGNAL(finished()), src, SLOT(deleteLater()));
    // Run, Forest, run!
    //src->start(); // This invokes WorkerThread::run in a new thread
}

/*
class WorkerThread : public QThread {
    void run() {
        while(1) {
             // ... hard work
             // Now want to notify main thread:
             QThread::msleep(200);
             int x;
             x = 99;
             emit progressChanged(x);
        }
    }
    // Define signal:
    signals:
    void progressChanged(int info);
};*/
