#include "makeprinter.h"
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

void run() {
    while(1) {
         // ... hard work
         // Now want to notify main thread:
         QThread::msleep(200);
         int x;
         x = 99;
         //emit progressChanged(x);
    }
}

long bar()
{
float x;
x = 0;
std::ifstream infile("C:\\Users\\Master\\Git\\retr3d\\logs\\retr3d.log");
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
    cout<<(x*1.176)<<endl;
    log = log + seglist[2] + "\n";
}
//cout << log << endl;
long y;
y=ceil(x*1.176);
return y;
}

char const*status()
{
int x;
x = 0;
std::ifstream infile("C:\\Users\\Master\\Git\\retr3d\\logs\\retr3d.log");
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
    cout << "import sys" << endl;
    PyRun_SimpleString("import os");
    cout << "import os" << endl;
    PyRun_SimpleString("sys.path.append('C:\\\\Users\\\\Master\\\\Git\\\\retr3d\\\\')");
    cout << "append" << endl;
    PyRun_SimpleString("execfile('C:\\\\Users\\\\Master\\\\Git\\\\retr3d\\\\makePrinter.py')");
    cout << "execfile" << endl;

    Py_Finalize();
}
