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

#ifndef MAKEPRINTER_H
#define MAKEPRINTER_H

#include <QMainWindow>
#include <QObject>
#include <QSharedDataPointer>
#include <QWidget>
#include <QMutex>
#include <iostream>

using namespace std;

class makePrinterData;

class makePrinter
{
public:
    makePrinter();
    makePrinter(const makePrinter &);
    makePrinter &operator=(const makePrinter &);
    ~makePrinter();

public slots:
    void onProgressChagned(int info);

private:
    QSharedDataPointer<makePrinterData> data;
};

void foo();
long bar();
char const*status(string str);
char const*scriptPath(string str);

#endif // MAKEPRINTER_H
