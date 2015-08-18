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
#include "makeprinter.h"
#include "mainwindow.h"
#include <iostream>
#include <thread>
#include <Python.h>
#include <sstream>
#include <string>
#include <fstream>
#include "QThread"
#include <math.h>
using namespace std;


class makePrinterData : public QSharedData
{
public:

};

makePrinter::makePrinter() : data(new makePrinterData)
{

}

makePrinter::makePrinter(const makePrinter &rhs) : data(rhs.data)
{

}

makePrinter &makePrinter::operator=(const makePrinter &rhs)
{
    if (this != &rhs)
        data.operator=(rhs.data);
    return *this;
}

makePrinter::~makePrinter()
{

}


long bar()
{
float x;
x = 0;
string str = path;
string pat = string(scriptPath(str))+"logs\\retr3d.log";
std::ifstream infile(pat);
string log;
std::string line;
while (std::getline(infile, line))
{
    std::istringstream iss(line);
    std::stringstream test(line);
    std::string segment;
    std::vector<std::string> seglist;

    while(std::getline(test, segment, ':'))
    {
       seglist.push_back(segment);


    }
    x=x+1;
    //cout<<(x*1.176)<<endl;
    log = log + seglist[2] + "\n";
}
//cout << log << endl;
long y;
y=ceil(x*1.176);
return y;
}

char const*scriptPath(string str)
{
    size_t index = 0;
    while (true) {
         /* Locate the substring to replace. */
         index = str.find("/", index);
         if (index == std::string::npos) break;

         /* Make the replacement. */
         str.replace(index, 1, "\\");

         /* Advance index forward so the next iteration doesn't pick it up as well. */
         index += 3;
    }
    str =  str+"\\";
    return str.c_str();
}

char const*status(string str)
{
int x;
x = 0;

string pat = string(scriptPath(str))+"logs\\retr3d.log";
std::ifstream infile(pat);
string log;
string logEnd;
std::string line;
while (std::getline(infile, line))
{
    std::istringstream iss(line);
    std::stringstream test(line);
    std::string segment;
    std::vector<std::string> seglist;

    while(std::getline(test, segment, ':'))
    {
       seglist.push_back(segment);

    }
    x=x+1;
    log = log + seglist[2] + "\n";
    logEnd = seglist[2];

}
//cout << log << endl;
return logEnd.c_str();
}

void foo()
{
    Py_Initialize();

    PyRun_SimpleString("import sys");
    PyRun_SimpleString("import os");
    string str = path;
    size_t index = 0;
    while (true) {
         /* Locate the substring to replace. */
         index = str.find("/", index);
         if (index == std::string::npos) break;

         /* Make the replacement. */
         str.replace(index, 1, "\\\\");

         /* Advance index forward so the next iteration doesn't pick it up as well. */
         index += 3;
    }
    str =  str+"\\\\";

    PyRun_SimpleString(("sys.path.append('"+str+"')").c_str());
    PyRun_SimpleString(("execfile('"+str+"makePrinter.py')").c_str());

    Py_Finalize();
}
