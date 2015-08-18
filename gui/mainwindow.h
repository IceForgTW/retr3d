#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QThread>
#include "makeprinter.h"
#include "worker.h"

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

public slots:
    void onProgressChanged(QString info);

private slots:
    void on_pushButton_clicked();

    void on_next1_clicked();

    void on_quit_clicked();

    void on_filesDir_push_clicked();

    void on_freecadDir_push_clicked();

    void on_next2_clicked();

    void on_next3_clicked();

    void updateProgress();

void startWorkInAThread();


private:
    Ui::MainWindow *ui;
    /**
     * @brief Thread object which will let us manipulate the running thread
     */
    QThread *thread;
    /**
     * @brief Object which contains methods that should be runned in another thread
     */
    Worker *worker;
};
#endif // MAINWINDOW_H
