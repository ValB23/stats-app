import pickle
import random
import sys
from PyQt5 import Qt, QtGui
from PyQt5.QtCore import qrand
from PyQt5.QtGui import QPainter, QColor, QPixmap, QIcon
from PyQt5.QtWidgets import *
from datetime import datetime


class histo:
    """ Histo class used to store the histogram"""

    def __init__(self):
        # print("__init__() method of the histo class.")
        self.list = []
        self.size = 0
        self.max = 0
        # Any variables below are used for the stats window, only used for when the list is sorted.
        self.min = 0
        self.mean = 0
        self.first_quartile = 0
        self.third_quartile = 0


class mainWindow(QMainWindow):
    """ Main app class """

    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.pieAct = QAction(" &Pie", self)
        self.histAct = QAction(" &Bar", self)
        self.clearAct = QAction(" &Clear", self)
        self.colorAct = QAction(" &Color", self)
        self.restoreAct = QAction(" &Restore", self)
        self.saveAct = QAction(" &Save", self)
        self.openAct = QAction(" &Open", self)
        self.exitAct = QAction(" &Exit", self)
        self.setWindowIcon(QtGui.QIcon('icon.png'))

        # Attributes of the main window
        self.setGeometry(300, 300, 600, 450)
        self.titleMainWindow = datetime.now().strftime("  %H:%M:%S ") + ' | Res: ' + str(
            self.width()) + 'x' + str(self.height())
        self.setWindowTitle(self.titleMainWindow)

        # Status bar to show some information.
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Information area")

        # When started, the program is in histogram mode
        self.isHisto = True

        self.pixmap = QPixmap(16, 16)
        self.colorIcon = QColor(255, 0, 0)
        self.pixmap.fill(self.colorIcon)
        self.Icon = QIcon(self.pixmap)

        # Creation of the histogram instance
        self.histo = histo()

        self.createActions()
        self.createMenus()
        self.setAcceptDrops(True)

    # Might be deleted if no potential uses are found.
    def resizeEvent(self, event):
        self.titleMainWindow = datetime.now().strftime("  %H:%M:%S") + '| Res: ' + str(
            self.width()) + 'x' + str(self.height())
        self.setWindowTitle(self.titleMainWindow)

    def createActions(self):

        # File action menu
        self.exitAct.setShortcut("Ctrl+Q")
        self.exitAct.triggered.connect(self.exit)

        self.openAct.setShortcut("Ctrl+O")
        self.openAct.triggered.connect(self.open)

        self.saveAct.setShortcut("Ctrl+S")
        self.saveAct.triggered.connect(self.save)

        self.restoreAct.setShortcut("Ctrl+E")
        self.restoreAct.triggered.connect(self.restore)

        # Display action menu
        self.colorAct.setShortcut("Ctrl+C")
        self.colorAct.triggered.connect(self.color)
        self.colorAct.setIcon(self.Icon)
        self.colorAct.setIconVisibleInMenu(True)

        self.clearAct.setShortcut("Ctrl+L")
        self.clearAct.triggered.connect(self.clear)

        # Draw action menu
        self.histAct.setShortcut("Ctrl+B")
        self.histAct.triggered.connect(self.histogram)

        self.pieAct.setShortcut("Ctrl+P")
        self.pieAct.triggered.connect(self.pie)

        # Stats action menu

    def createMenus(self):
        """ Create the menus and its items """

        fileMenu = self.menuBar().addMenu("&File")
        fileMenu.addAction(self.openAct)
        fileMenu.addAction(self.saveAct)
        fileMenu.addAction(self.restoreAct)
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAct)

        menuDisplay = self.menuBar().addMenu("&Display")
        menuDisplay.addAction(self.colorAct)
        menuDisplay.addAction(self.clearAct)

        menuDisplay = self.menuBar().addMenu("&Draw")
        menuDisplay.addAction(self.histAct)
        menuDisplay.addAction(self.pieAct)

        menuDisplay = self.menuBar().addMenu("&Stats")

        menuDisplay = self.menuBar().addMenu("&About")

    def open(self):
        """ Associated slot of openAct, instance of QAction """

        filename = QFileDialog.getOpenFileName(self, 'Open file', './', "files (*.dat)")
        self.statusBar.showMessage("Open")
        self.histo.list = []
        self.histo.size = 0
        if filename[0]:
            f = open(filename[0], 'r')
            lines = f.readlines()
            for line in lines:
                self.histo.list.append(int(line))
            self.histo.size = len(self.histo.list)
            self.histo.max = int(max(self.histo.list))
            self.histo.sum = sum(self.histo.list)
            f.close()
            self.statusBar.showMessage("Histogram opened " + self.histo.sum.__str__())

    def drawHistogram(self):
        column = int(self.width() / self.histo.size)
        qp = QPainter()
        qp.begin(self)
        qp.setPen(QColor(0, 0, 0))
        qp.setBrush(self.colorIcon)
        for i in range(self.histo.size):
            qp.drawRect(i * column, self.height() - self.statusBar.height(), column, - int(
                int(self.histo.list[i]) * (self.height() - self.statusBar.height() - 30) / self.histo.max))
        qp.end()

    def drawPie(self):
        spaceq = 360 * 16 / self.histo.sum
        qp = QPainter()
        qp.begin(self)
        qp.setPen(QColor(0, 0, 0))
        currentAngle = 0
        for i in range(self.histo.size):
            qp.setBrush(QColor(qrand() % 256, qrand() % 256, qrand() % 256))
            # Pie = (x, y, width, height, startAngle, spanAngle)
            qp.drawPie(self.statusBar.height() + 3, self.statusBar.height() + 3,
                       self.width() - 2 * self.statusBar.height() - 3, self.height() - 2 * self.statusBar.height() - 3,
                       int(currentAngle), int(self.histo.list[i] * spaceq))
            currentAngle += self.histo.list[i] * spaceq

        qp.end()

    def serialize(self):
        open('saveHisto.bin', 'w').close()
        file = open("saveHisto.bin", "wb")
        pickle.dump(self.histo.list, file)

    def save(self):
        """ Slot associé à saveAct, instance de QAction"""

        self.serialize()
        self.statusBar.showMessage("Histogram saved")

    def restore(self):
        """ Slot associé à restoreAct, instance de QAction"""

        self.deserialize()
        self.update()
        self.statusBar.showMessage("Histogram restored")

    def deserialize(self):
        self.histo.list = []
        self.histo.size = 0
        self.histo.max = 0
        file = open("saveHisto.bin", "rb")
        self.histo.list = pickle.load(file)
        self.histo.max = int(max(self.histo.list))
        self.histo.size = len(self.histo.list)
        self.histo.sum = sum(self.histo.list)

    def exit(self):
        """ Slot associé à exitAct, instance de QAction"""

        self.statusBar.showMessage("Quit")
        QApplication.quit()

    def color(self):
        """ Slot associé à colorAct, instance de QAction"""

        self.statusBar.showMessage("Color")
        self.colorIcon = QColorDialog.getColor(self.colorIcon)
        self.pixmap.fill(self.colorIcon)
        self.Icon = QIcon(self.pixmap)
        self.colorAct.setIcon(self.Icon)
        self.update()

    def clear(self):
        """ Slot associé à clearAct, instance de QAction"""

        self.statusBar.showMessage("Histogram cleared")
        self.histo.list = []
        self.histo.size = 0
        self.histo.max = 0
        self.update()

    def randomizeHisto(self):
        if self.histo.size > 0:
            for i in range(self.histo.size):
                self.histo.list[i] = random.randint(0, 99)
            self.histo.max = int(max(self.histo.list))
            self.histo.sum = sum(self.histo.list)

    def keyPressEvent(self, event):
        if event.key() == Qt.Qt.Key_R:
            self.statusBar.showMessage("Histogram randomize")
            self.randomizeHisto()
            self.update()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            filename = url.toLocalFile()
            self.statusBar.showMessage("Drop file: " + filename)
            if filename[0] and filename.endswith(".dat"):
                f = open(filename, 'r')
                lines = f.readlines()
                self.histo.list = []
                self.histo.size = 0
                self.histo.max = 0
                for line in lines:
                    self.histo.list.append(int(line))
                self.histo.size = len(self.histo.list)
                self.histo.max = int(max(self.histo.list))
                self.histo.sum = sum(self.histo.list)
                f.close()
                self.statusBar.showMessage("Drop file: " + filename + " accepted")
                self.update()

    def histogram(self):
        """ Slot associé à histoAct, instance de QAction"""

        self.statusBar.showMessage("Histogramme")
        self.isHisto = True
        self.update()

    def pie(self):
        """ Slot associé à pieAct, instance de QAction"""

        self.statusBar.showMessage("Pie")
        self.isHisto = False
        self.update()

    def paintEvent(self, event):
        self.titlestart = str(self.height()) + " " + str(self.width()) + " " + datetime.now().strftime(
            "  %H:%M:%S")
        self.setWindowTitle(self.titlestart)

        # If there's a histogram opened, restored or dropped into the app, drawing will start.
        # If the app is in Pie mode, a pie chart will be displayed instead of a histogram.
        if self.histo.list:
            if self.isHisto:
                self.setMinimumHeight(0)
                self.setMinimumWidth(0)
                self.setMaximumHeight(10000)
                self.setMaximumWidth(10000)
                self.drawHistogram()
            else:
                self.setMinimumHeight(800)
                self.setMinimumWidth(800)
                self.setMaximumHeight(800)
                self.setMaximumWidth(800)
                self.drawPie()

    def stats(self, event):
        self.statusBar.showMessage("Stats")
        # Opens a window showing some basic stats of the current histogram / file opened
        # TODO: Display max, min, average, median, quartiles, etc.
        # self.histo.max
        # self.histo.min
        # self.mean
        # self.histo.first_quartile
        # self.histo.third_quartile


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = mainWindow()
    w.show()
    app.exec_()
