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
#include <windows.h>
#include <fstream>
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
    Py_Finalize();
    remove( "globalVars.pyc" );
    delete ui;
}

void MainWindow::onProgressChanged(QString info) {
    // Processing code
    ui->printerProgress->setValue(info.toInt());
    string str;
    str = ui->scriptsDir->text().toStdString();
    ui->progressLabel->setText(status(str));
}

void MainWindow::on_pushButton_clicked()
{
    ui->stackedWidget->setCurrentIndex(1);
}

void MainWindow::on_next2_clicked()
{
    ofstream gv;
    gv.open ("globalVars.py");


  gv << "from __future__ import division # allows floating point division from integers                                                                                         \n";
  gv << "reloadClasses = False                                                                                                                                                  \n";
  gv << "test = None                                                                                                                                                            \n";
  gv << "                                                                                                                                                                       \n";
  gv << "#Change the following to the path to the directory that will hold your printer designs                                                                                 \n";
  gv << "#Make sure to use forward slashes like this / and not back slashes like this \\                                                                                         \n";
  size_t index = 0;
  string str;
  str = ui->freecadDir->text().toStdString();
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
  gv << "freecadDir = '"+str+"'                                                                                                            \n";
  index = 0;
  str = ui->filesDir->text().toStdString();
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
  gv << "printerDir = '"+str+"'                                                                                                                \n";
  gv << "                                                                                                                                                                       \n";
  gv << "#Output Options                                                                                                                                                        \n";
  gv << "level = 2                                                                                                                                                              \n";
  gv << "                                                                                                                                                                       \n";
  gv << "#make test hole pattern. True if you would like the test hole pattern to be included in your stl files                                                                 \n";
  gv << "printTestHolePattern = True                                                                                                                                            \n";
  gv << "                                                                                                                                                                       \n";
  gv << "#xRod vars                                                                                                                                                             \n";
  gv << "xRodDiaTop = "+ui->xRodDiaTop->text().toStdString()+" #Diameter of the top xRod                                                                                                                             \n";
  gv << "xRodDiaBottom = "+ui->xRodDiaBottom->text().toStdString()+" #Diameter of the bottom xRod                                                                                                                       \n";
  gv << "xRodLength = "+ui->xRodLength->text().toStdString()+" # Length of the shorter xRod                                                                                                                          \n";
  gv << "xRodDiaMax = None 					#CALCULATED The largest xRod diameter                                                                                               \n";
  gv << "xMotorShaftToMountHoleDistX = None 	#CALCULATED The horizontal component of the distance between the shaft and the mounting holes                                   \n";
  gv << "xMotorBodyWidth = None 				#CALCULATED Width of the xMotors body                                                                                           \n";
  gv << "xRodSpacing = None 					#CALCULATED The distance between the axes of the xRods.                                                                         \n";
  gv << "                                                                                                                                                                       \n";
  gv << "#yRod vars                                                                                                                                                             \n";
  gv << "yRodDiaL = 12.7 #Diameter of the top yRod                                                                                                                              \n";
  gv << "yRodDiaR = 12.7 #Diameter of the bottom yRod                                                                                                                           \n";
  gv << "yRodLength = 460 # Length of the shorter yRod                                                                                                                          \n";
  gv << "yRodSpacing = None	#CALCULATED Distance between yRods                                                                                                                  \n";
  gv << "yRodDiaMax = None 	#CALCULATED largest yRod diameter                                                                                                                   \n";
  gv << "yBushingNutMaxThickness = None #Calculated The maximum thickness of the y bushing nuts                                                                                 \n";
  gv << "                                                                                                                                                                       \n";
  gv << "#zRod vars                                                                                                                                                             \n";
  gv << "zRodDiaR = 12.7 #Diameter of the right zRod                                                                                                                            \n";
  gv << "zRodDiaL = 12.7 #Diameter of the left zRod                                                                                                                             \n";
  gv << "zRodLength = 460 #Length of the shorter zRod                                                                                                                           \n";
  gv << "zRodSpacing = None	#CALCULATED Distance between zRod axes                                                                                                              \n";
  gv << "zRodStandoff = None	#CALCULATED Distance between frame surface and zRod Axis                                                                                        \n";
  gv << "                                                                                                                                                                       \n";
  gv << "#Lead Screw Related                                                                                                                                                    \n";
  gv << "leadScrewDia = 6.35 #Diameter of the leadScrew                                                                                                                         \n";
  gv << "zRodZScrewDist = None #CALCULATED Distance between the axis of the zRod and the axis of the LeadScrew. Increased if needed                                             \n";
  gv << "                                                                                                                                                                       \n";
  gv << "                                                                                                                                                                       \n";
  gv << "#Frame vars                                                                                                                                                            \n";
  gv << "frameWidth = 20 #Width of frame members on the face to which the y and z axes are attached.                                                                            \n";
  gv << "frameHeight = 19.05#Height of frame members. This is the 2nd cross sectional dimension                                                                                 \n";
  gv << "frameThickness = 1.33 #Thickness of frame wall if frame is hollow.                                                                                                     \n";
  gv << "frameJointPadding = 10 #ADVANCED Required distance at frame joints for welds which might get in the way of mounted parts                                               \n";
  gv << "                                                                                                                                                                       \n";
  gv << "                                                                                                                                                                       \n";
  gv << "#Mounting nut and bolt info                                                                                                                                            \n";
  gv << "mountToPrintedDia = 3 #Actual diameter of holes that are used to mount items to printed parts. IE other printed parts or sheet metal.                                  \n";
  gv << "mountToFrameDia = 4.12 #Actual diameter of holes that are used to mount items to the frame. Printed parts to frame or sheet metal to frame.                            \n";
  gv << "mountToPrintedPadding = 3	#ADVANCED the minimum distance between the edge of a hole and the edge of the part                                                          \n";
  gv << "printedToFrameDia = None 	#CALCULATED The adjusted diameter for printed parts that will be mounted to the frame.                                                      \n";
  gv << "printedToPrintedDia = None 	#CALCULATED The adjusted diameter for printed parts mounted to other printed parts or to non frame parts                                \n";
  gv << "                                                                                                                                                                       \n";
  gv << "                                                                                                                                                                       \n";
  gv << "#rodClamps - much of this should be combined with mounting bolt info above                                                                                             \n";
  gv << "clampHoleDia = 3.5 				#ADVANCED Diameter of clamping holes on rod clamps and endStop mounts                                                               \n";
  gv << "clampNutPadding = 3 			#ADVANCED The minimum wall thickness for the clamp nut cut out                                                                          \n";
  gv << "clampNutFaceToFace = 5.6 		#ADVANCED Face to face distance of clamp nuts                                                                                           \n";
  gv << "clampNutThickness = 2.5 		#ADVANCED The thickness of the clamp nuts                                                                                               \n";
  gv << "clampGap = 2 					#ADVANCED The gap between the support and the clamp                                                                                     \n";
  gv << "clampThickness = 3 				#ADVANCED The clamp thickness on rod clamps                                                                                         \n";
  gv << "clampBoltHeadThickness = 3 		#ADVANCED The thickness of the head of the clamp bolts                                                                              \n";
  gv << "rodSupportNutTrapDepthMin = 5 	#ADVANCED The minimum value the rod support nut trap depth can take                                                                     \n";
  gv << "rodSupportNutTrapDepthMax = 10 	#ADVANCEDthe maximum value the rod support nut trap depth can take                                                                  \n";
  gv << "#rodSupportNutTrapDepth = 5 	#CALCULATED The depth of the nut traps on the rod supports                                                                              \n";
  gv << "rodSupportClampThickness = 2 	#ADVANCED The thickness of plastic below the rod that is clamped. Basically the clamping thickness but in the support.                  \n";
  gv << "                                                                                                                                                                       \n";
  gv << "                                                                                                                                                                       \n";
  gv << "#mounting tabs - much of this should be combined with mounting bolt info above                                                                                         \n";
  gv << "#SlotDia should be printedToFrameDia                                                                                                                                   \n";
  gv << "slotDia = 4.55 		#ADVANCED The diameter of the mounting slots                                                                                                    \n";
  gv << "tabThickness = 4 	#ADVANCED The thickness of the mounting tabs                                                                                                        \n";
  gv << "slotWidth = 3.5		#ADVANCED The width of the mounting slots                                                                                                       \n";
  gv << "slotPadding = 3 	#ADVANCED Amount of material to sides of slot                                                                                                       \n";
  gv << "                                                                                                                                                                       \n";
  gv << "                                                                                                                                                                       \n";
  gv << "#PrintBedRelated                                                                                                                                                       \n";
  gv << "printBedMountHoleDia = 3 #Diameter of mounting bolts                                                                                                                   \n";
  gv << "printBedThickness = 1.5 #Thickness of heated print bed plate                                                                                                           \n";
  gv << "printBedPadding = 5 			#ADVANCED extra space around the perimiter of the printBed that is not printable.                                                       \n";
  gv << "printBedMountHolePadding = 1.5 	#ADVANCED Distance from edge of print bed to edge of mounting hole                                                                  \n";
  gv << "printBedStandoff = 10 			#ADVANCED The distance between the top of the print bed support and the print bed                                                       \n";
  gv << "printableWidth = None			#CALCULATED printable dimension in the x direction                                                                                      \n";
  gv << "printableLength = None			#CALCULATED printable dimension in the y direction                                                                                      \n";
  gv << "printableHeight = None			#CALCULATED printable dimension in the z direction                                                                                      \n";
  gv << "                                                                                                                                                                       \n";
  gv << "#printBedBushingHolder related                                                                                                                                         \n";
  gv << "PBBHStandoff = None #Calculated The distance from the bottom of the printBedSupport to the axis of the yRod                                                            \n";
  gv << "printBedBusingSupportWidth = None #The width of the printBedBushingSupport                                                                                             \n";
  gv << "PBBHMaxFaceToFace = None                                                                                                                                               \n";
  gv << "PBBHDepth = None #CALCULATED the depth of the printBedBushingHolder                                                                                                    \n";
  gv << "                                                                                                                                                                       \n";
  gv << "#PrintBedSupport related                                                                                                                                               \n";
  gv << "printBedSupportThickness = 1.55 #The thickness of the printBedSupport plate                                                                                            \n";
  gv << "yBushingNutSeparation = None #Calculated the distance between bushing nuts on the same rod                                                                             \n";
  gv << "                                                                                                                                                                       \n";
  gv << "#xRodClamp                                                                                                                                                             \n";
  gv << "xRodClampIdlerHoleDia = 3.5 #The diameter of the xRodClamp idler hole                                                                                                  \n";
  gv << "xRodClampThickness = 3.5 					#ADVANCED Thickness of plastic around the largest diameter rod                                                              \n";
  gv << "xRodClampPocketDepth = 25 				#ADVANCED Distance the xRods are inserted into the xRodClamp                                                                    \n";
  gv << "xRodClampMountHoleToEdgePadding = 3 	#ADVANCED Distance from side of xRodClamp to mountHole edge(ie not center)                                                      \n";
  gv << "xRodClampMountHoleToRodPadding = 1.5	#ADVANCED The vertical distance from the edge of the largest xRod to the edges of the mounting holes                            \n";
  gv << "xRodClampEdgeToMountHoleDist = 4.75 	#ADVANCED Distance from xRodClamp side to mounting holes.THIS SHOULD BE CHANGED TO PADDING                                      \n";
  gv << "xRodClampMountHoleToRodPadding = 1.5 	#ADVANCED                                                                                                                       \n";
  gv << "xRodClampExtraPocketDepth = 3 			#ADVANCED Extra distance in the pocket as an allowance.                                                                         \n";
  gv << "xRodClampWidth = None					#CACLULATED Width of the xRodClamp                                                                                              \n";
  gv << "xRodClampOverallThickness = None		#CALCULATED The thickness of the xRodClamp                                                                                      \n";
  gv << "xRodAxisToMountHoleDist = None			#CALCULATED Distance from x Rod axis to mount hole centers in vertical direction                                                \n";
  gv << "                                                                                                                                                                       \n";
  gv << "                                                                                                                                                                       \n";
  gv << "#xEndMotorPlate                                                                                                                                                        \n";
  gv << "xEndIdlerHoleDia = 3 #Diameter of idler hole (as apposed to printed which is larger)                                                                                   \n";
  gv << "xMotorMountPlateThickness = 3.175 #The thickness of the xMotorMountPlate (idler plate too)                                                                             \n";
  gv << "xMotorMountPlateWidth = 50.8 #The width of the xMotorMountPlate                                                                                                        \n";
  gv << "xEndNumMountHoles = 4 # The number of motor mount holes on the xEnd motor                                                                                              \n";
  gv << "xEndShaftToMountHoleDist = 21.92 #The distance from the shaft to the mount holes                                                                                       \n";
  gv << "xEndMotorMountHoleDia = 3 # the x motor mount hole diameter                                                                                                            \n";
  gv << "xEndMotorMountHolePadding = 4.4 #The distance between the motor mount holes and the edge of the plate                                                                  \n";
  gv << "xMotorPulleyDia = 12.1  # The diameter of the xMotor Pully                                                                                                             \n";
  gv << "motorToXRodClampSpacing = 12 #ADVANCED The gap between the xEnd motor and the xRodClamp                                                                                \n";
  gv << "                                                                                                                                                                       \n";
  gv << "                                                                                                                                                                       \n";
  gv << "#xEndZRodHolder                                                                                                                                                        \n";
  gv << "xEndZRodHolderFaceThickness = 3  #The thickness of the face of the xEndZRodHolder                                                                                      \n";
  gv << "xEndZRodHolderMountHoletoEdgePadding = 3 #horizontal distance from edge of xEndZRodHolder to the edges of mounting holes                                               \n";
  gv << "xEndZRodHolderMountHoleToRodPadding = 1.5 #The vertical distance from the edge of the largest xRod to the edges of the mounting holes                                  \n";
  gv << "#The above should be consolidated with the xRodClampEdgeToMountHoleDist and xRodAxisToMountHoleDist                                                                    \n";
  gv << "zOffsetNutThickness = 3 #The thickness of the zOffsetNut                                                                                                               \n";
  gv << "zOffsetNutFaceToFace = 5.6 #The face to face distance of the zOffsetNut                                                                                                \n";
  gv << "zOffsetHoleDia = 3.5 #The hole diameter of the xOffSet bolt                                                                                                            \n";
  gv << "zMotorBodyToFrameSpacing = 5 			#ADVANCED The space between the zMotor and the frame.                                                                           \n";
  gv << "zBushingNutMaxFaceToFace = None			#CACLULATED The max Face to face distance between the two z bushing nut sizes                                               \n";
  gv << "zBushingNutMaxThickness = None			#CACLULATED The max thickness for the z Bushing nuts                                                                            \n";
  gv << "xEndZRodHolderMaxNutThickness = None	#CACLULATED The max nut thickness for the xEndZRodHolder                                                                        \n";
  gv << "xEndZRodHolderMaxNutFaceToFace = None	#CACLULATED The max Nut face to face for the xEndZRodHolder                                                                     \n";
  gv << "xEndZRodHolderHeight = None				#CACLULATED The height of the xEndZRodHolder                                                                                \n";
  gv << "                                                                                                                                                                       \n";
  gv << "#xCarriage                                                                                                                                                             \n";
  gv << "xCarriageWidth = 65 					#ADVANCED The width of the xCarriage not including wings                                                                        \n";
  gv << "xCarriageThickness = 6 					#ADVANCED The thickness of the xCarriage face                                                                               \n";
  gv << "xBeltAnchorThickness = 6 				#ADVANCED The thickness of the belt anchor                                                                                      \n";
  gv << "xBeltAnchorSlotWidth = 6 				#ADVANCED The width of the slot in the belt anchor                                                                              \n";
  gv << "xBeltAnchorSlotInset = 6 				#ADVANCED The distance from the edge of the anchor to the slot                                                                  \n";
  gv << "xBeltAnchorBridgeThickness = 3 			#ADVANCED The thickness of the belt anchor bridge                                                                           \n";
  gv << "xCarriageWingWidth = 10 				#ADVANCED The width of the xCarriage wings                                                                                      \n";
  gv << "xCarriageWingHeight = 10 				#ADVANCED The height of the xCarriage wings                                                                                     \n";
  gv << "xBeltAnchorWidthTop = 18 				#ADVANCED Should be CALCULATED - The width of the top of the belt anchor                                                        \n";
  gv << "xBeltAnchorWidthBottom = 25				#ADVANCED Should be CALCULATED - The width of the bottom of the belt anchor                                                 \n";
  gv << "xCarriageMountHoleVertOffset = 20 		#ADVANCED Should be CALCULATED - The distance from the bottom edge of the face to the extruder mounting holes                   \n";
  gv << "xCarriageMountHoleHorizOffset = 4.75	#ADVANCED Should be CALCULATED - The distance from the side of the xCarriage and the extruder mounting holes                    \n";
  gv << "xBushingNutMaxFacetoFace = None	#CALCULATED The maximum xBushing nut face to face distance                                                                          \n";
  gv << "xBushingNutMaxThickness = None	#CALCULATED The maximum bushing nut thickness for the x axis                                                                            \n";
  gv << "xCarriageBushingHolderOR = None	#CALCULATED the bushing holder outside radius on the x carriage                                                                     \n";
  gv << "xBeltAnchorHeight = None		#CALCULATED The height of the belt anchor from the back of the xCarriage face                                                           \n";
  gv << "                                                                                                                                                                       \n";
  gv << "                                                                                                                                                                       \n";
  gv << "#zMotorMount vars                                                                                                                                                      \n";
  gv << "#needs a plate thickness                                                                                                                                               \n";
  gv << "zMotorMountHoles = 4 #The number of motor mounting holes                                                                                                               \n";
  gv << "zShaftToMountHoleDist = 21.92 #the distance between the shaft and the mounting holes                                                                                   \n";
  gv << "zMotorMountHoleDia = 3.5	#the diameter of the motor mounting holes                                                                                                   \n";
  gv << "zMotorMountHolePadding = 4.39 # the minimum space between the edge of the motor mounting holes and the edge of the plate                                               \n";
  gv << "zMotorMountPlateThickness= 6 #The thickness of the z motor mount plate                                                                                                 \n";
  gv << "zMotorMountPlateWidth= 42.5 #Width of motor mount plate                                                                                                                \n";
  gv << "zMotorMountShaftHoleDia = 24 #Diameter of the shaft hole in the zMotorMount.                                                                                           \n";
  gv << "zMotorMountLocation = 'Bottom' 		#ADVANCED The location of the zMotorMounts. Either Top or Bottom                                                                \n";
  gv << "zMotorMountLength = None 			#CALCULATED The length of the z motor mount plate                                                                                   \n";
  gv << "zMotorMountMountingFaceWidth = None	#Calculated The width of the frame member to which the z motor mount is attached                                                \n";
  gv << "zMotorMountEdgeToShaftHole = None 	#CALCULATED The distance from the frame side edge of the motor mount to the shaft hole center                                       \n";
  gv << "zShaftToMountHoleDistX = None 		#Calculated                                                                                                                         \n";
  gv << "zMotorBodyWidth = None 				#CALCULATED Width of the zMotorBody                                                                                             \n";
  gv << "                                                                                                                                                                       \n";
  gv << "#yMotorMount vars                                                                                                                                                      \n";
  gv << "#needs a plate thickness                                                                                                                                               \n";
  gv << "yShaftToMountHoleDist = 33.195 #the distance between the shaft and the mounting holes                                                                                  \n";
  gv << "yMotorMountHolePadding = 4.39 #The distance between the edge of the motor and the edge of the motor mount holes                                                        \n";
  gv << "yMotorMountHoleDia = 4.4 # Dia of the y motor mount holes                                                                                                              \n";
  gv << "yMotorMountPlateWidth = 57 # The width of the y motor mount plate                                                                                                      \n";
  gv << "yMotorMountPlateThickness = 6 #Thickness of the yMotorMountPlate                                                                                                       \n";
  gv << "yMotorMountShaftHoleDia = 24 #The diameter of the shaft hole for the y motor mount                                                                                     \n";
  gv << "yMotorMountHoles = 4 # The number of motor mounting holes for the y motor                                                                                              \n";
  gv << "yMotorPulleyDia = 19.5 #The diameter of the y motor pulley                                                                                                             \n";
  gv << "yMotorShaftToMountHoleDistX = None	#CALCULATED The x component of the distance from the shaft to the mount hole                                                        \n";
  gv << "yMotorBodyWidth = None				#CALCULATED The width of the y motor body                                                                                           \n";
  gv << "                                                                                                                                                                       \n";
  gv << "                                                                                                                                                                       \n";
  gv << "#zRodSupport vars                                                                                                                                                      \n";
  gv << "zRodSupportLength = 15 #ADVANCED The length of the zrod that is supported                                                                                              \n";
  gv << "                                                                                                                                                                       \n";
  gv << "                                                                                                                                                                       \n";
  gv << "#YRodSupport vars                                                                                                                                                      \n";
  gv << "yRodSupportClearance = 3 			#ADVANCED The clearance between the top of the clamping bolts and the bottom of the printBedSupport.                                \n";
  gv << "yRodSupportWidth = None				#CALCULATED The total width of the Rod Support including tabs.                                                                  \n";
  gv << "yRodStandoff = None					#CALCULATED The distance from the top of the frame to the yRod axis                                                             \n";
  gv << "yRodSupportMountHoleSpacing = None	#CALCULATED The center to center distance for the yRodSupport mounting holes. Middle of slot to middle of slot                      \n";
  gv << "yRodSupportClampBoltLength = None	#CALCULATED The length of the clamping bolts used for the yRodClamps                                                                \n";
  gv << "yRodSupportNutTrapDepth = None 		#CALCULATED The depth of the nut traps on the rod supports                                                                      \n";
  gv << "                                                                                                                                                                       \n";
  gv << "                                                                                                                                                                       \n";
  gv << "#yBeltAnchor                                                                                                                                                           \n";
  gv << "yBeltAnchorWidth = 6 			#ADVANCED The width of the belt anchor column                                                                                           \n";
  gv << "yBeltAnchorLength = 24 			#ADVANCED The length of the belt anchor Column                                                                                      \n";
  gv << "yBeltAnchorBridgeThickness = 3 	#ADVANCED The thickness of the y belt anchor bridge                                                                                 \n";
  gv << "yBeltAnchorSlotWidth = 6 		#ADVANCED The width of the y belt anchor slot                                                                                           \n";
  gv << "yBeltAnchorHoleSpacing = None	#CALCULATED Center to center distance between yBeltAnchorHoles                                                                          \n";
  gv << "yBeltAnchorHeight = None		#CALCULATED The total height (including tab thickness) of the y belt anchor                                                             \n";
  gv << "                                                                                                                                                                       \n";
  gv << "                                                                                                                                                                       \n";
  gv << "#extruderMountPlate vars                                                                                                                                               \n";
  gv << "extruderMountPlateThickness = 1.55 #The thickness of the extruderMountPlate                                                                                            \n";
  gv << "hotEndMountHoleDia = 3 #The diameter of the hot end mounting holes                                                                                                     \n";
  gv << "extruderMountPlateWidth = None	#CALCULATED The width of the extrtuder mount plate                                                                                      \n";
  gv << "                                                                                                                                                                       \n";
  gv << "                                                                                                                                                                       \n";
  gv << "#extruderMountAngle vars                                                                                                                                               \n";
  gv << "extruderMountAngleWidth = 19.05 # The width of the angle used. (The nominal size of the angle.)                                                                        \n";
  gv << "extruderMountAngleThickness = 3.175 # The thickness of the angle used.                                                                                                 \n";
  gv << "                                                                                                                                                                       \n";
  gv << "                                                                                                                                                                       \n";
  gv << "#extruder vars                                                                                                                                                         \n";
  gv << "extruderWidth = 78 #The width of the extruder body                                                                                                                     \n";
  gv << "extruderDepth = 55 # The required depth for mounting the extruder front edge of body to back most part of extruder                                                     \n";
  gv << "extruderMountHoleSpacing = 48 #The distance between the extruder's mounting holes                                                                                      \n";
  gv << "extruderMountHoleDia = 3 #The diameter of the extruder's mounting holes                                                                                                \n";
  gv << "extruderFilamentHoleDia = 4 #The diameter of extruder's filament hole                                                                                                  \n";
  gv << "extruderEdgeToCenterLine = 14 #The distance from the outer edge of the extruder to it's center line                                                                    \n";
  gv << "extruderNozzleStandoff = None	#CALCULATED The distance from the center of the nozzle to the face of the vertical bars                                                 \n";
  gv << "                                                                                                                                                                       \n";
  gv << "                                                                                                                                                                       \n";
  gv << "#extruderBarrel vars                                                                                                                                                   \n";
  gv << "extruderBarrelDia = 25.4 #Diameter of the extruder barrel                                                                                                              \n";
  gv << "extruderBarrelLength = 42 #The length of the extruderBarrel                                                                                                            \n";
  gv << "extruderBarrelLinerDia = 6.35 #The diameter of the teflon barrel liner                                                                                                 \n";
  gv << "extruderBarrelNumFins = 7 #The number of cooling fins not including the top and bottom faces.                                                                          \n";
  gv << "extruderBarrelFaceThickness = 3 #The thickness of the top and bottom faces                                                                                             \n";
  gv << "extruderBarrelCoreThickness = 1.5 #The thickness of metal around the barrel liner                                                                                      \n";
  gv << "extruderBarrelFinGap = 3.175 #The space between fins                                                                                                                   \n";
  gv << "extruderBarrelMountHoleDia = 2.5 #Diameter of mounting holes for extruder barrel. 2.5mm hole will be tapped to 3mm                                                     \n";
  gv << "extruderBarrelMountHoleDepth = 10 #the depth of the mounting holes.                                                                                                    \n";
  gv << "hotEndMountHoleSpacing = 20 # The center to center distance between the hot end mounting holes                                                                         \n";
  gv << "                                                                                                                                                                       \n";
  gv << "                                                                                                                                                                       \n";
  gv << "#nozzle vars                                                                                                                                                           \n";
  gv << "nozzleBodyHeight = 10 #The height of the nozzle body                                                                                                                   \n";
  gv << "nozzleBodyWidth = 19.05 #The width of the nozzle body                                                                                                                  \n";
  gv << "nozzleBodyDepth = 12.7 #The depth of the nozzle body                                                                                                                   \n";
  gv << "nozzleResistorDia = 6.5 #The diameter of the heater resistor                                                                                                           \n";
  gv << "nozzleResistorInset = 5 #The distance between the axis of the resistor and the outer edge of the heater block                                                          \n";
  gv << "nozzleThermistorDia = 1.5 #The diameter of the Thermistor bead                                                                                                         \n";
  gv << "nozzleThermistorDepth = 3 #The depth of the thermistor mount hole                                                                                                      \n";
  gv << "nozzleThermistorRetainerDia = 2.5 #The diameter of the thermistor retainer screw                                                                                       \n";
  gv << "nozzleThermistorRetainerDepth = 3 #The depth of the thermistor retainer hole                                                                                           \n";
  gv << "nozzleDia = .4 #The diameter of the nozzle                                                                                                                             \n";
  gv << "nozzleBaseDia = 8.35 #The diameter of the nozzle base                                                                                                                  \n";
  gv << "nozzleStepDia = 3 #The diameter of the step down from the barrel liner. This should be just a bit larger than the filament diameter                                    \n";
  gv << "nozzleStepOffset = 1 #The distance from the tip of the setp hole to the tip of the nozzle                                                                              \n";
  gv << "nozzleDrillAngle = 118 #The drill point angle of the drill bits used                                                                                                   \n";
  gv << "nozzleTipDia = 1 #The diameter of the flat surrounding the nozzle's hole                                                                                               \n";
  gv << "nozzleThermistorHoleVertOffset = 2 #The distance from the lower edge of the heater block to the center of the thermistor hole.                                         \n";
  gv << "nozzleThermistorRetainerHorizOffset = 3 #The distance from the outer edge of the heater block to the center of the retainer hole.                                      \n";
  gv << "nozzleLength = 15	#CALCULATED The total length of the nozzle                                                                                                          \n";
  gv << "                                                                                                                                                                       \n";
  gv << "                                                                                                                                                                       \n";
  gv << "#hotEnd vars                                                                                                                                                           \n";
  gv << "hotEndLength = None #CALCULATED The total length of the hot end from the nozzle to the top of the barrel                                                               \n";
  gv << "                                                                                                                                                                       \n";
  gv << "                                                                                                                                                                       \n";
  gv << "#Cross bar vars                                                                                                                                                        \n";
  gv << "yBeltIdlerHoleDia = 6 #The diameter of the hole for the yBeltIdler                                                                                                     \n";
  gv << "crossBarLength = None #CALCULATED The length of the cross bars                                                                                                         \n";
  gv << "                                                                                                                                                                       \n";
  gv << "                                                                                                                                                                       \n";
  gv << "#Side bar vars                                                                                                                                                         \n";
  gv << "sideBarLength = None #CALCULATED The length of the side bars                                                                                                           \n";
  gv << "                                                                                                                                                                       \n";
  gv << "                                                                                                                                                                       \n";
  gv << "#frameSpacer vars                                                                                                                                                      \n";
  gv << "#frameSpacerLength should be calculated depending on the power supply thickness, electronics or motors                                                                 \n";
  gv << "frameSpacerLength = 90 # The length of the frameSpacers                                                                                                                \n";
  gv << "frameSpacerOffset = 10 # The distancebetween the end of the sideBar to the edge of the frameSpacer                                                                     \n";
  gv << "                                                                                                                                                                       \n";
  gv << "                                                                                                                                                                       \n";
  gv << "#xEndstop vars                                                                                                                                                         \n";
  gv << "xEndstopHeight = 4.5 # The height of the body of the endstop                                                                                                           \n";
  gv << "xEndstopContactSpacing = 3 # The distance between the contact strips. Surface to surface not center to center                                                          \n";
  gv << "xEndstopChannelWidth = 0.5 # The width of the channels for the metal contact strips                                                                                    \n";
  gv << "xEndstopChannelDepth = 3 #The depth of the channels for the metal contact strips                                                                                       \n";
  gv << "xEndstopPadding = 1.5 # The minimum distance between the edge of a feature (hole or channel) and the edge of the endstop                                               \n";
  gv << "xEndstopCapThickness = 2 #The thickness of the endstop cap                                                                                                             \n";
  gv << "xEndstopLength = None	#CALCULATED The length of the body of the endstop                                                                                               \n";
  gv << "                                                                                                                                                                       \n";
  gv << "                                                                                                                                                                       \n";
  gv << "#zEndStop vars                                                                                                                                                         \n";
  gv << "zEndstopJogWidth = 2 #The width of the jog used to trap the contacts                                                                                                   \n";
  gv << "zEndstopSupportWidth = None		#CALCULATED The width of the zEndstop                                                                                               \n";
  gv << "zEndStopClampLength = None		#CALCULATED The length along the z axis of the zEndStop clamp                                                                           \n";
  gv << "zEndstopBodyThickness = None 	#CALCULATED The thickness of the zEndstop between the zRod and the zEndStopCap                                                          \n";
  gv << "                                                                                                                                                                       \n";
  gv << "#LeadScrewCoupler vars                                                                                                                                                 \n";
  gv << "leadScrewCouplerLength = 25 #The length (vertical axis) of the leadScrewCouplers                                                                                       \n";
  gv << "leadScrewCouplerGap = 5 #The space above and below the leadScrewCoupler. For keeping the coupler from  crashing into zMotor mount plate or xCarriage                   \n";
  gv << "                                                                                                                                                                       \n";
  gv << "#Hole Calibration table                                                                                                                                                \n";
  gv << "#small hole diameters are adjusted for printed parts using this array.                                                                                                 \n";
  gv << "holeAdjust = [[1,0],                                                                                                                                                   \n";
  gv << "              [2,1.38],                                                                                                                                                \n";
  gv << "              [3,2.44],                                                                                                                                                \n";
  gv << "              [4,3.53],                                                                                                                                                \n";
  gv << "              [5,4.45],                                                                                                                                                \n";
  gv << "              [6,5.6],                                                                                                                                                 \n";
  gv << "              [7,6.7],                                                                                                                                                 \n";
  gv << "              [8,7.6],                                                                                                                                                 \n";
  gv << "              [9,8.64],                                                                                                                                                \n";
  gv << "              [10,9.5],                                                                                                                                                \n";
  gv << "              [11,10.64],                                                                                                                                              \n";
  gv << "              [12,11.6]]                                                                                                                                               \n";
  gv << "                                                                                                                                                                       \n";
  gv << "                                                                                                                                                                       \n";
  gv << "#bushing nut lookup related                                                                                                                                            \n";
  gv << "bushingNutSizesUsed = 'Standard' # The type of bushing nuts used in the printer, standard, metric or standardAndMetric                                                 \n";
  gv << "bushingNutTable = [] #The table of bushing nuts used to build the printer.                                                                                             \n";
  gv << "                                                                                                                                                                       \n";
  gv << "                                                                                                                                                                       \n";
  gv << "#Standard Nut Sizes [Thread dia, Minor dia, Face to face, Thickness] in inches (will be converted)                                                                     \n";
  gv << "standardNuts = [[0.1120, 0.0939, 1/4 , 3/32], #4                                                                                                                       \n";
  gv << "                [0.1380, 0.1140, 5/16 , 7/64], #6                                                                                                                      \n";
  gv << "                [0.1640, 0.1390, 11/32, 1/8], #8                                                                                                                       \n";
  gv << "                [0.1900, 0.1560, 3/8 , 1/8],#10                                                                                                                        \n";
  gv << "                [0.2160, 0.181, 7/16, 5/32], #12                                                                                                                       \n";
  gv << "                [1/4, 0.2070, 7/16, 7/32],                                                                                                                             \n";
  gv << "                [5/16,0.2650, 1/2, 17/64],                                                                                                                             \n";
  gv << "                [3/8, 0.321, 9/16, 21/64],                                                                                                                             \n";
  gv << "                [7/16,0.376, 11/16, 3/8],                                                                                                                              \n";
  gv << "                [1/2,0.434, 3/4, 7/16],                                                                                                                                \n";
  gv << "#				[9/16,0.490, 7/8, 31/64],	#commented out because this size is uncommon                                                                                \n";
  gv << "                [5/8,0.546, 15/16, 35/64]                                                                                                                              \n";
  gv << "                ]                                                                                                                                                      \n";
  gv << "                                                                                                                                                                       \n";
  gv << "                                                                                                                                                                       \n";
  gv << "#Metric Nut Sizes [Thread dia, Minor dia, Face to face, Thickness] in mm                                                                                               \n";
  gv << "metricNuts =   [[2.5, 1.993, 5, 2],                                                                                                                                    \n";
  gv << "                [3,2.439, 5.5, 2.4],                                                                                                                                   \n";
  gv << "#				[3.5, 2.829, 6, 2.8], #NOT COMMON                                                                                                                       \n";
  gv << "                [4, 3.220, 7, 3.2],                                                                                                                                    \n";
  gv << "                [5, 4.110, 8, 4],                                                                                                                                      \n";
  gv << "                [6, 4.891, 10, 5],                                                                                                                                     \n";
  gv << "                [8, 6.619, 13, 6.5],                                                                                                                                   \n";
  gv << "                [10, 8.344, 17, 8],                                                                                                                                    \n";
  gv << "                [12, 10.072, 19, 10],                                                                                                                                  \n";
  gv << "                [14, 11.797, 22, 11],                                                                                                                                  \n";
  gv << "                [16, 13.797, 24, 13]                                                                                                                                   \n";
  gv << "                ]                                                                                                                                                      \n";
  gv << "                                                                                                                                                                       \n";
  gv << "                                                                                                                                                                       \n";
  gv << "#Lengths of bolts available                                                                                                                                            \n";
  gv << "standardBoltLengths = [.5, .75, 1, 1.25, 1.5, 2] #in inches (will be converted to mm)                                                                                  \n";
  gv << "metricdBoltLengths = [10,12,16,20,25,30,35,40]                                                                                                                         \n";
  gv << "clampBoltLengths = [10,12,16,20,25,30,35,40]                                                                                                                           \n";
  gv << "                                                                                                                                                                       \n";
  gv << "#BushingNut and leadScrew related                                                                                                                                      \n";
  gv << "bushingNutPadding = 5 # minimum thickness of holder around nut and thickness of depth stop                                                                             \n";
  gv << "bushingNutRodGap = 1 #extra radius in the hole for the smooth rod                                                                                                      \n";
  gv << "xBushingNutBottom = None	#CALCULATED Bushing nut dimensions selected from the nut tables depends on rod dia                                                          \n";
  gv << "xBushingNutTop = None 		#CALCULATED Bushing nut dimensions selected from the nut tables depends on rod dia                                                          \n";
  gv << "yBushingNutR = None			#CALCULATED Bushing nut dimensions selected from the nut tables depends on rod dia                                                      \n";
  gv << "yBushingNutL = None			#CALCULATED Bushing nut dimensions selected from the nut tables depends on rod dia                                                      \n";
  gv << "zBushingNutR = None			#CALCULATED Bushing nut dimensions selected from the nut tables depends on rod dia                                                      \n";
  gv << "zBushingNutL = None			#CALCULATED Bushing nut dimensions selected from the nut tables depends on rod dia                                                      \n";
  gv << "leadScrewNut = None			#CALCULATED Leas screw nut dimensions selected from the nut tables depends on screw dia                                                 \n";
  gv << "                                                                                                                                                                       \n";
  gv << "                                                                                                                                                                       \n";
  gv << "#Colors colors are in % RGB                                                                                                                                            \n";
  gv << "printedR = 255/255                                                                                                                                                     \n";
  gv << "printedG = 253/255                                                                                                                                                     \n";
  gv << "printedB = 232/255                                                                                                                                                     \n";
  gv << "printedA = 0.0 #doesn't seem to do anything!!!                                                                                                                         \n";
  gv << "                                                                                                                                                                       \n";
  gv << "frameR = 0/255                                                                                                                                                         \n";
  gv << "frameG = 0/255                                                                                                                                                         \n";
  gv << "frameB = 156/255                                                                                                                                                       \n";
  gv << "frameA = 0.0 #doesn't seem to do anything!!!                                                                                                                           \n";
  gv << "                                                                                                                                                                       \n";
  gv << "                                                                                                                                                                       \n";
  gv << "#Verticle Bar vars                                                                                                                                                     \n";
  gv << "vertBarDistAboveZRod = None #CALCULATED The distance from the top of the zRods to the top edge of the vertical bar                                                     \n";
  gv << "vertBarDistBelowZRod = None #CALCULATED The distance from the bottom of the zRods to the bottom edge of the vertical bar                                               \n";
  gv << "vertBarLength = None #CALCULATED The length of the vertical bar                                                                                                        \n";
  gv << "                                                                                                                                                                       \n";
  gv << "                                                                                                                                                                       \n";
  gv << "#Parts lists                                                                                                                                                           \n";
  gv << "xAxisParts = []                                                                                                                                                        \n";
  gv << "yAxisParts = []                                                                                                                                                        \n";
  gv << "zAxisParts = []                                                                                                                                                        \n";
  gv << "                                                                                                                                                                       \n";
  gv << "#Plater Variables                                                                                                                                                      \n";
  gv << "plate = False #To Plate or not to Plate, that is the Question                                                                                                          \n";
  gv << "platerName = 'plater' #Name of actual Plater file, eg 'plater' 'plater.exe' 'plater.app'                                                                               \n";
  gv << "platerWidth = 150 #width, width of the plate, in mm (default 150)                                                                                                      \n";
  gv << "platerHeight = 150 #height of the plate, in mm (default 150)                                                                                                           \n";
  gv << "platerPrecision = 0.5 #precision, in mm (default 0.5)                                                                                                                  \n";
  gv << "platerSpacing = 2 #parts spacing, in mm (default 2)                                                                                                                    \n";
  gv << "platerDelta = 2 #sets the spacing of the brute forcing (see below), default 2mm                                                                                        \n";
  gv << "platerRotation = 90 #sets the angle of the brute forcing, default 90                                                                                                   \n";
  gv << "                                                                                                                                                                       \n";
  gv << "#Slic3r Variables                                                                                                                                                      \n";
  gv << "slic3r = False #Slice or nah?                                                                                                                                          \n";
  gv << "sli3erName = 'slic3r' #Name of actual Slic3r file, eg 'slic3r' 'slic3r.exe' 'slic3r.app'                                                                               \n";
  gv << "sli3erVars = ''                                                                                                                                                        \n";
  gv << "                                                                                                                                                                       \n";
  gv << "#Zip Variables                                                                                                                                                         \n";
  gv << "zipName = 'Printer_Files' #Name of zip file                                                                                                                            \n";

     gv.close();


    ui->stackedWidget->setCurrentIndex(3);
    QFuture<void> t1 = QtConcurrent::run(foo);
    // To avoid having two threads running simultaneously, the previous thread is aborted.
    worker->abort();

    //ui->printerProgress->setValue(10);
    thread->wait(); // If the thread is not running, this will immediately return.

    worker->requestWork();
}

void MainWindow::on_next1_clicked()
{
    ui->stackedWidget->setCurrentIndex(2);
    QValidator *validator = new QIntValidator(0, 9999, this);
    ui->xRodDiaTop->setValidator(validator);
    ui->xRodDiaBottom->setValidator(validator);
    ui->xRodLength->setValidator(validator);
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
    if(!(ui->scriptsDir->text().isEmpty())&&!(ui->freecadDir->text().isEmpty())){ui->next1->setEnabled(true);}else{ui->next1->setEnabled(false);}
}

void MainWindow::on_freecadDir_push_clicked()
{
    QString dir = QFileDialog::getExistingDirectory(this, tr("Open Directory"),
                                                 "/home",
                                                 QFileDialog::ShowDirsOnly
                                                 | QFileDialog::DontResolveSymlinks);
    ui->freecadDir->setText(dir);
    if(!(ui->filesDir->text().isEmpty())&&!(ui->scriptsDir->text().isEmpty())){ui->next1->setEnabled(true);}else{ui->next1->setEnabled(false);}
}

void MainWindow::on_scriptsDir_push_clicked()
{
    QString dir = QFileDialog::getExistingDirectory(this, tr("Open Directory"),
                                                 "/home",
                                                 QFileDialog::ShowDirsOnly
                                                 | QFileDialog::DontResolveSymlinks);
    ui->scriptsDir->setText(dir);
    if(!(ui->filesDir->text().isEmpty())&&!(ui->freecadDir->text().isEmpty())){ui->next1->setEnabled(true);}else{ui->next1->setEnabled(false);}
}

class GUIUpdater : public QObject {
    Q_OBJECT

public:
    explicit GUIUpdater(QObject *parent = 0) : QObject(parent) {}
    void newLabel(const QString &image) { emit requestNewLabel(image); }

signals:
    void requestNewLabel(const QString &);
};

void MainWindow::on_xRodDiaTop_textChanged(const QString &arg1)
{
    if(!(ui->xRodDiaTop->text().isEmpty())&&!(ui->xRodDiaBottom->text().isEmpty())&&!(ui->xRodLength->text().isEmpty())){ui->next2->setEnabled(true);}else{ui->next2->setEnabled(false);}
}

void MainWindow::on_xRodDiaBottom_textChanged(const QString &arg1)
{
    if(!(ui->xRodDiaTop->text().isEmpty())&&!(ui->xRodDiaBottom->text().isEmpty())&&!(ui->xRodLength->text().isEmpty())){ui->next2->setEnabled(true);}else{ui->next2->setEnabled(false);}
}

void MainWindow::on_xRodLength_textChanged(const QString &arg1)
{
    if(!(ui->xRodDiaTop->text().isEmpty())&&!(ui->xRodDiaBottom->text().isEmpty())&&!(ui->xRodLength->text().isEmpty())){ui->next2->setEnabled(true);}else{ui->next2->setEnabled(false);}
}

