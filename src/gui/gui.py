import sys
import webbrowser
import gmplot
import os

import networkx as nx
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QFileDialog, QComboBox, QLineEdit, QWidget, QVBoxLayout, QDialog, QLabel, QPushButton
from PyQt5.QtGui import QFont, QFontMetrics
from PyQt5 import uic
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from src.core import algorithm as algo, Area as area, Components as comp, function as func, parsing as parse
from src.places import itbBdg as gane, itbNangor as nangor, alunalun as alun


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi("./src/gui/gui.ui", self)

        # Initiate attributes
        self.costResult = 0
        self.pathResult = []
        self.nodeNameUI = []
        self.graphUI = None

        #label input
        self.input = self.findChild(QPushButton, "pushButton")
        self.input.clicked.connect(self.pushInputFile)

        #label ucs
        self.ucs = self.findChild(QPushButton, "pushButton_2")
        self.ucs.clicked.connect(self.on_ucs_clicked)
        self.ucs.clicked.connect(self.plot_graph)

        #label a*
        self.a = self.findChild(QPushButton, "pushButton_3")
        self.a.clicked.connect(self.on_a_clicked)
        self.a.clicked.connect(self.plot_graph)

        #dropdown
        self.dropdown = self.findChild(QComboBox, "comboBox_2")
        self.dropdown.addItems(["Input File", "ITB Ganesha", "ITB Jatinangor", "Alun-Alun Bandung", "Bandung Selatan", "Cilacap"])
        self.dropdown.currentIndexChanged.connect(self.dropdownChanged)

        #graph
        self.widget = self.findChild(QWidget, "widget")
        self.widget.setGeometry(800,370,993,645)
    
        #start
        self.start = self.findChild(QLineEdit, "lineEdit_3")
        
        #goal
        self.goal = self.findChild(QLineEdit, "lineEdit")

        #show gmap
        self.gmap = self.findChild(QPushButton, "pushButton_4")
        self.gmap.clicked.connect(self.showGmap)

        # cost
        self.cost = self.findChild(QLabel, "label_10")
        
        self.label_9 = self.findChild(QLabel, "label_9")

        # path
        self.path = self.findChild(QLabel, "label_11")

        self.show()
    
    def showErrorMessage(self, message):
        dialog = QDialog(self)
        dialog.setWindowTitle("Error")
        layout = QVBoxLayout(dialog)
        layout.addWidget(QLabel(message))
        button = QPushButton("OK", dialog)
        button.clicked.connect(dialog.accept)
        layout.addWidget(button)
        dialog.exec_()
        
    # input file
    def pushInputFile(self):
        self.nodeNameUI = []
        try :
            inputFile = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', "Text files (*.txt)")
            if inputFile:
                self.graphUI = parse.parse_adjacency_matrix(inputFile[0])
                for i in range(len(self.graphUI.getListNode())):
                    self.nodeNameUI.append(self.graphUI.getNameNode(i))
        except :
            self.showErrorMessage("Please input file first")
            raise

    # input start
    def input(self):
        global input
        input = self.start.text()
        
    # input goal
    def goal(self):
        global goal
        goal = self.goal.text()

    #plot graph
    def plot_graph(self):
        Graph = nx.Graph()
        for i in Graph.nodes():
            Graph.nodes[i]['label'] = self.nodeNameUI[i]
        for i in range(len(self.nodeNameUI)):
            for j in range(i+1, len(self.nodeNameUI)):
                if self.graphUI.getMatrix()[i][j] != 0:
                    Graph.add_edge(self.nodeNameUI[i], self.nodeNameUI[j], weight=self.graphUI.getMatrix()[i][j])
        fig = Figure(figsize=(10,5.3), dpi=100)
        canvas = FigureCanvas(fig)
        pos = nx.spring_layout(Graph)
        ax = fig.add_subplot(111)
        edge_colors = ['red' if (u, v) in zip(self.pathResult, self.pathResult[1:]) else 'black' for u, v in Graph.edges()]
        nx.draw_networkx_edge_labels(Graph, pos, edge_labels=nx.get_edge_attributes(Graph, 'weight'))
        nx.draw(Graph, pos, with_labels=True, node_size=300, node_color='green', edge_color=edge_colors, font_size=10, ax=ax)
        plt.axis('off')
        canvas.setParent(self.widget)
        canvas.show()

    def initiateMapToGraph(self, place: area.Area):
        self.nodeNameUI = []
        nodeList = func.initiateListNode(place.getListName(), place.getMatrix())
        self.graphUI = comp.Graph(place.getMatrix(), nodeList)
        self.graphUI.convertCoordinatesToWAM(place.getListCoordinate())
        for i in range(len(self.graphUI.getListNode())):
            self.nodeNameUI.append(self.graphUI.getNameNode(i))
    
    #dropdown
    def dropdownChanged(self):
        if self.dropdown.currentText() == "Input File":
            pass
        else:
            global place

            if self.dropdown.currentText() == "ITB Ganesha":
                place = area.Area(gane.x, gane.y, gane.zoom, gane.listKoordinat, gane.listNodeName, gane.matriks)

            elif self.dropdown.currentText() == "ITB Jatinangor":
                place = area.Area(nangor.x, nangor.y, nangor.zoom, nangor.listKoordinat, nangor.listNodeName, nangor.matriks)

            elif self.dropdown.currentText() == "Alun-Alun Bandung":
                place = area.Area(alun.x, alun.y, alun.zoom, alun.listKoordinat, alun.listNodeName, alun.matriks)

            elif self.dropdown.currentText() == "Bandung Selatan":
                pass
            elif self.dropdown.currentText() == "Cilacap":
                pass

            self.initiateMapToGraph(place)

    #ucs
    def chooseUCS(self):
        cost = 0
        path = []
        try:
            cost, path = algo.uniform_cost_search(self.graphUI, self.start.text(), self.goal.text())

            font = QFont()
            font.setPointSize(10)
            self.cost.setFont(font)
            self.cost.setText(str(cost))
            self.path.setFont(font)
            self.path.setText(str(path))
            self.path.setAdjustSize(True)
        
        except:
            if self.start.text() == "":
                self.showErrorMessage("Start is empty")

            elif self.start.text() not in self.nodeNameUI:
                self.showErrorMessage("Start is not in the node")

            if self.goal.text() == "":
                self.showErrorMessage("Goal is empty")

            elif self.goal.text() not in self.nodeNameUI:
                self.showErrorMessage("Goal is not in the node")
        
        return cost, path
            

    #astar
    def chooseA(self):
        cost = 0
        path = []
        try:
            cost, path = algo.a_star(self.graphUI, self.start.text(), self.goal.text())

            font = QFont()
            font.setPointSize(10)
            self.cost.setFont(font)
            self.cost.setText(str(cost))
            self.path.setFont(font)
            self.path.setText(str(path))
            self.path.setAdjustSize(True)
        
        except:
            if self.start.text() == "":
                self.showErrorMessage("Start is empty")

            elif self.start.text() not in self.nodeNameUI:
                self.showErrorMessage("Start is not in the node")

            if self.goal.text() == "":
                self.showErrorMessage("Goal is empty")

            elif self.goal.text() not in self.nodeNameUI:
                self.showErrorMessage("Goal is not in the node")
        
        return cost, path

    # Assign costResult and pathResult on click event
    def on_ucs_clicked(self):
        self.costResult, self.pathResult = self.chooseUCS()
        print(self.costResult, self.pathResult)

    def on_a_clicked(self):
        self.costResult, self.pathResult = self.chooseA()

    # show gmap
    def showGmap(self):
        try:
            gmap = gmplot.GoogleMapPlotter(place.getCenter()[0], place.getCenter()[1], place.getZoom())
            for i in range(len(self.graphUI.getMatrix())):
                for j in range(len(self.graphUI.getMatrix())):
                    if(self.graphUI.getMatrix()[i][j] > 0):
                        latitude = [place.getListCoordinate()[i][0],place.getListCoordinate()[j][0]]
                        longitude = [place.getListCoordinate()[i][1],place.getListCoordinate()[j][1]]
                        gmap.scatter(latitude, longitude, 'yellow', size = 7, marker = False)
                        gmap.plot(latitude, longitude, 'blue', edge_width = 3)

            for k in range(len(place.getMatrix())):
                gmap.text(place.getListCoordinate()[k][0], place.getListCoordinate()[k][1], place.getListName()[k])

            for i in range(len(self.pathResult)-1):
                x = place.getListName().index(self.pathResult[i])
                y = place.getListName().index(self.pathResult[i+1])
                latitude = [place.getListCoordinate()[x][0],place.getListCoordinate()[y][0]]
                longitude = [place.getListCoordinate()[x][1],place.getListCoordinate()[y][1]]
                gmap.scatter(latitude, longitude, 'orange', size = 7, marker = True)
                gmap.plot(latitude, longitude, 'red', edge_width = 3)

            gmap.draw("./mymap.html")

            webbrowser.open_new_tab('file://' + os.path.realpath('mymap.html'))
        except:
            self.showErrorMessage("Please choose the algorithm")
            raise

def initiateUI():
    app = QApplication(sys.argv)
    window = UI()
    sys.exit(app.exec_())

if __name__ == '__main__':
    # import sys
    app = QApplication(sys.argv)
    window = UI()
    sys.exit(app.exec_())
