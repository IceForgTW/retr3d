#ifndef MAKEPRINTER_H
#define MAKEPRINTER_H

#include <QMainWindow>
#include <QObject>
#include <QSharedDataPointer>
#include <QWidget>

class makePrinterData;

class makePrinter
{
public:
    makePrinter();
    makePrinter(const makePrinter &);
    makePrinter &operator=(const makePrinter &);
    ~makePrinter();

private:
    QSharedDataPointer<makePrinterData> data;
};

void foo();

#endif // MAKEPRINTER_H
