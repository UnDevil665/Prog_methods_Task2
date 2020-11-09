from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.formLayout = QtWidgets.QFormLayout(self.centralwidget)
        self.formLayout.setObjectName("formLayout")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Graph view"))


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.view = GraphicsView()
        self.formLayout.addWidget(self.view)


class GraphicsView(QtWidgets.QGraphicsView):
    def __init__(self, widget: QtWidgets.QWidget = 0):
        super(GraphicsView, self).__init__()
        self.setMinimumSize(100, 100)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.scene = QtWidgets.QGraphicsScene()
        self.setScene(self.scene)

        self.group1 = QtWidgets.QGraphicsItemGroup()
        self.group2 = QtWidgets.QGraphicsItemGroup()

        self.scene.addItem(self.group1)
        self.scene.addItem(self.group2)

        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(True)
        self.timer.start(50)

        self.timer.timeout.connect(self.slotAlarmTimer)

    def slotAlarmTimer(self):
        self.deleteItemsFromGroup(self.group1)
        self.deleteItemsFromGroup(self.group2)

        width = self.width()
        height = self.height()

        self.scene.setSceneRect(0, 0, width, height)

        penBlack = QtGui.QPen(QtCore.Qt.black)
        penRed = QtGui.QPen(QtCore.Qt.red)
        self.group1.addToGroup(self.scene.addLine(20, 20, width - 20, 20, penBlack))
        self.group1.addToGroup(self.scene.addLine(width - 20, 20, width - 20, height - 20, penBlack))
        self.group1.addToGroup(self.scene.addLine(width - 20, height - 20, 20, height - 20, penBlack))
        self.group1.addToGroup(self.scene.addLine(20, height - 20, 20, 20, penBlack))

    def deleteItemsFromGroup(self, group):
        for i in self.scene.items(group.boundingRect()):
            if i.group() == group:
                del i

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        self.timer.start(50)
        QtWidgets.QGraphicsView.resizeEvent(self, event)

