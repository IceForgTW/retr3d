#include "makeprinter.h"
#include <iostream>
#include <thread>
#include <Python.h>
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

void foo()
{
    Py_Initialize();

    PyRun_SimpleString("import sys");
    PyRun_SimpleString("import os");
    PyRun_SimpleString("sys.path.append('C:\\\\Users\\\\Master\\\\Git\\\\retr3d\\\\')");
    PyRun_SimpleString("execfile('C:\\\\Users\\\\Master\\\\Git\\\\retr3d\\\\makePrinter.py')");

    Py_Finalize();
}

