#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

private slots:
    void on_pushButton_clicked();

    void on_next1_clicked();

    void on_quit_clicked();

    void on_filesDir_push_clicked();

    void on_freecadDir_push_clicked();

    void on_next2_clicked();

    void on_next3_clicked();

private:
    Ui::MainWindow *ui;
};

#endif // MAINWINDOW_H
