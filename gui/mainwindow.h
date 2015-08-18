/*
Copyright 2015.
   - Primarily authored by Michael Uttmark

This file is part of Retr3d, a program to 3D model printable parts for the construction of 3D printers.
See https://github.com/Maaphoo/Retr3d for more information.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This progra is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QThread>
#include "makeprinter.h"
#include "worker.h"

extern string path;

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

void on_xRodDiaTop_textChanged(const QString &arg1);

void on_xRodDiaBottom_textChanged(const QString &arg1);

void on_xRodLength_textChanged(const QString &arg1);

void on_scriptsDir_push_clicked();

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
