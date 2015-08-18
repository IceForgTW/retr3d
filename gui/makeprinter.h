#ifndef MAKEPRINTER_H
#define MAKEPRINTER_H

#include <QMainWindow>
#include <QObject>
#include <QSharedDataPointer>
#include <QWidget>
#include <QMutex>

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
char const*status();

#endif // MAKEPRINTER_H
