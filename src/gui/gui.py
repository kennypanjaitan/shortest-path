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


        #label input
        self.input = self.findChild(QPushButton, "pushButton")
        self.input.clicked.connect(self.pushInputFile)

        #label ucs
        self.ucs = self.findChild(QPushButton, "pushButton_2")
        self.ucs.clicked.connect(self.chooseUCS)
        self.ucs.clicked.connect(self.plot_graph)

        #label a*
        self.a = self.findChild(QPushButton, "pushButton_3")
        self.a.clicked.connect(self.chooseA)
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
    
    # input file
    def pushInputFile(self):
        global input
        global matrix
        global node
        try :
            node = []
            file = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', "Text files (*.txt)")
            if file:
                input = parse.parse_adjacency_matrix(file[0])
                matrix = input.getMatrix()
                for i in range(len(input.getListNode())):
                    node.append(input.getNameNode(i))
        except :
            dialog = QDialog(self)
            dialog.setWindowTitle("Error")
            layout = QVBoxLayout(dialog)
            layout.addWidget(QLabel("Please input file first"))
            button = QPushButton("OK", dialog)
            button.clicked.connect(dialog.accept)
            layout.addWidget(button)
            dialog.exec_()

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
        global path
        Graph = nx.Graph()
        for i in Graph.nodes():
            Graph.nodes[i]['label'] = node[i]
        for i in range(len(node)):
            for j in range(i+1, len(node)):
                if matrix[i][j] != 0:
                    Graph.add_edge(node[i], node[j], weight=matrix[i][j])
        fig = Figure(figsize=(10,5.3), dpi=100)
        canvas = FigureCanvas(fig)
        pos = nx.spring_layout(Graph)
        ax = fig.add_subplot(111)
        edge_colors = ['red' if (u, v) in zip(path, path[1:]) else 'black' for u, v in Graph.edges()]
        nx.draw_networkx_edge_labels(Graph, pos, edge_labels=nx.get_edge_attributes(Graph, 'weight'))
        nx.draw(Graph, pos, with_labels=True, node_size=300, node_color='green', edge_color=edge_colors, font_size=10, ax=ax)
        plt.axis('off')
        canvas.setParent(self.widget)
        canvas.show()

    #dropdown
    def dropdownChanged(self):
        if self.dropdown.currentText() == "Input File":
            pass
        else:
            global input
            global matrix
            global node
            global place
            node = []

            if self.dropdown.currentText() == "ITB Ganesha":
                place = area.Area(gane.x, gane.y, gane.zoom, gane.listKoordinat, gane.listNodeName, gane.matriks)
                nodeList = func.initiateListNode(gane.listNodeName, gane.matriks)
                graph = comp.Graph(gane.matriks, nodeList)
                graph.convertCoordinatesToWAM(place.getListCoordinate())
                input = graph
                matrix = input.getMatrix()
                for i in range(len(input.getListNode())):
                    node.append(input.getNameNode(i))

            elif self.dropdown.currentText() == "ITB Jatinangor":
                place = area.Area(nangor.x, nangor.y, nangor.zoom, nangor.listKoordinat, nangor.listNodeName, nangor.matriks)
                nodeList = func.initiateListNode(nangor.listNodeName, nangor.matriks)
                graph = comp.Graph(nangor.matriks, nodeList)
                graph.convertCoordinatesToWAM(place.getListCoordinate())
                input = graph
                matrix = input.getMatrix()
                for i in range(len(input.getListNode())):
                    node.append(input.getNameNode(i))

            elif self.dropdown.currentText() == "Alun-Alun Bandung":
                place = area.Area(alun.x, alun.y, alun.zoom, alun.listKoordinat, alun.listNodeName, alun.matriks)
                nodeList = func.initiateListNode(alun.listNodeName, alun.matriks)
                graph = comp.Graph(alun.matriks, nodeList)
                graph.convertCoordinatesToWAM(place.getListCoordinate())
                input = graph
                matrix = input.getMatrix()
                for i in range(len(input.getListNode())):
                    node.append(input.getNameNode(i))

            elif self.dropdown.currentText() == "Bandung Selatan":
                pass
            elif self.dropdown.currentText() == "Cilacap":
                pass

    #ucs
    def chooseUCS(self):
        global cost
        global path
        try:
            cost, path = algo.uniform_cost_search(input, self.start.text(), self.goal.text())
            font = QFont()
            font.setPointSize(10)
            self.cost.setFont(font)
            self.cost.setText(str(cost))
            self.path.setFont(font)
            self.path.setText(str(path))
            self.path.setAdjustSize(True)

            return cost, path
        except:
            if self.start.text() == "":
                dialog = QDialog(self)
                dialog.setWindowTitle("Error")
                layout = QVBoxLayout(dialog)
                layout.addWidget(QLabel("Start is empty"))
                button = QPushButton("OK", dialog)
                button.clicked.connect(dialog.accept)
                layout.addWidget(button)
                dialog.exec_()
            elif self.start.text() not in node:
                dialog = QDialog(self)
                dialog.setWindowTitle("Error")
                layout = QVBoxLayout(dialog)
                layout.addWidget(QLabel("Start is not in the node"))
                button = QPushButton("OK", dialog)
                button.clicked.connect(dialog.accept)
                layout.addWidget(button)
                dialog.exec_()
            if self.goal.text() == "":
                dialog = QDialog(self)
                dialog.setWindowTitle("Error")
                layout = QVBoxLayout(dialog)
                layout.addWidget(QLabel("Goal is empty"))
                button = QPushButton("OK", dialog)
                button.clicked.connect(dialog.accept)
                layout.addWidget(button)
                dialog.exec_()
            elif self.goal.text() not in node:
                dialog = QDialog(self)
                dialog.setWindowTitle("Error")
                layout = QVBoxLayout(dialog)
                layout.addWidget(QLabel("Goal is not in the node"))
                button = QPushButton("OK", dialog)
                button.clicked.connect(dialog.accept)
                layout.addWidget(button)
                dialog.exec_()

    #astar
    def chooseA(self):
        global cost
        global path
        try:
            cost, path = algo.a_star(input, self.start.text(), self.goal.text())
            font = QFont()
            font.setPointSize(10)
            self.cost.setFont(font)
            self.cost.setText(str(cost))
            self.path.setFont(font)
            self.path.setText(str(path))
            self.path.setAdjustSize(True)
            return cost, path
        except:
            if self.start.text() == "":
                dialog = QDialog(self)
                dialog.setWindowTitle("Error")
                layout = QVBoxLayout(dialog)
                layout.addWidget(QLabel("Start is empty"))
                button = QPushButton("OK", dialog)
                button.clicked.connect(dialog.accept)
                layout.addWidget(button)
                dialog.exec_()
            elif self.start.text() not in node:
                dialog = QDialog(self)
                dialog.setWindowTitle("Error")
                layout = QVBoxLayout(dialog)
                layout.addWidget(QLabel("Start is not in the node"))
                button = QPushButton("OK", dialog)
                button.clicked.connect(dialog.accept)
                layout.addWidget(button)
                dialog.exec_()
            if self.goal.text() == "":
                dialog = QDialog(self)
                dialog.setWindowTitle("Error")
                layout = QVBoxLayout(dialog)
                layout.addWidget(QLabel("Goal is empty"))
                button = QPushButton("OK", dialog)
                button.clicked.connect(dialog.accept)
                layout.addWidget(button)
                dialog.exec_()
            elif self.goal.text() not in node:
                dialog = QDialog(self)
                dialog.setWindowTitle("Error")
                layout = QVBoxLayout(dialog)
                layout.addWidget(QLabel("Goal is not in the node"))
                button = QPushButton("OK", dialog)
                button.clicked.connect(dialog.accept)
                layout.addWidget(button)
                dialog.exec_()

        # show gmap
    def showGmap(self):
        try:
            map = gmplot.GoogleMapPlotter(place.getCenter()[0], place.getCenter()[1], place.getZoom())
            for i in range(len(place.getListCoordinate())):
                for j in range(len(place.getListCoordinate())):
                    if(nangor.matriks[i][j] == 1):
                        latitude = [place.getListCoordinate()[i][0],place.getListCoordinate()[j][0]]
                        longitude = [place.getListCoordinate()[i][1],place.getListCoordinate()[j][1]]
                        map.scatter(latitude, longitude, 'yellow', size = 7, marker = False)
                        map.plot(latitude, longitude, 'blue', edge_width = 3)
            for k in range(len(place.getListCoordinate())):
                map.text(place.getListCoordinate()[k][0], place.getListCoordinate()[k][1], place.getListName()[k])
            for i in range(len(path)-1):
                x = place.getListName().index(path[i])
                y = place.getListName().index(path[i+1])
                latitude = [place.getListCoordinate()[x][0],place.getListCoordinate()[y][0]]
                longitude = [place.getListCoordinate()[x][1],place.getListCoordinate()[y][1]]
                map.scatter(latitude, longitude, 'orange', size = 7, marker = True)
                map.plot(latitude, longitude, 'red', edge_width = 3)

            map.draw("./mymap.html")

            webbrowser.open_new_tab('file://' + os.path.realpath('mymap.html'))
        except:
            dialog = QDialog(self)
            dialog.setWindowTitle("Error")
            layout = QVBoxLayout(dialog)
            layout.addWidget(QLabel("Please choose the algorithm"))
            button = QPushButton("OK", dialog)
            button.clicked.connect(dialog.accept)
            layout.addWidget(button)
            dialog.exec_()

def initiateUI():
    app = QApplication(sys.argv)
    window = UI()
    sys.exit(app.exec_())

if __name__ == '__main__':
    # import sys
    app = QApplication(sys.argv)
    window = UI()
    sys.exit(app.exec_())
