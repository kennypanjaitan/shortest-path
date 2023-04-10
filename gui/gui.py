from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QFileDialog, QComboBox, QLineEdit, QGraphicsView, QWidget, QVBoxLayout, QGraphicsScene
from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QRectF
from PyQt5 import uic
import sys
sys.path.append('../src/')
import algorithm
import Components as comp
import parsing
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# class graphCanvas(QWidget):
#     def __init__(self, parent: None):
#         super().__init__(parent)
#         self.figure = plt.figure()
#         self.canvas = FigureCanvas(self.figure)
#         self.layout = QVBoxLayout(self)
#         self.layout.addWidget(self.canvas)

#         self.graph = nx.DiGraph(np.matrix(UI.matrix(self)))
#         self.pos = nx.spring_layout(self.graph)
#         self.ax = self.figure.add_subplot(111)
#         self.ax.set_title("Graph")
#         self.plot()

#     def plot(self):
#         self.ax.clear()
#         nx.draw(self.graph, self.pos, with_labels=True, node_size=30, node_color='red', font_size=10)
#         self.canvas.draw()


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi("../gui/gui.ui", self)


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
        self.dropdown = self.findChild(QComboBox, "comboBox")
        self.dropdown.addItems(["ITB", "Alun-Alun Bandung", "Bandung Selatan", "Jatinangor", "Input File"])
        self.dropdown.currentIndexChanged.connect(self.dropdownChanged)

        #graph
        self.widget = self.findChild(QWidget, "widget")
        self.widget.setGeometry(510,180,701,431)
    
        #start
        self.start = self.findChild(QLineEdit, "lineEdit")
        
        #goal
        self.goal = self.findChild(QLineEdit, "lineEdit_2")

        self.show()
    
        
    # input file
    def pushInputFile(self):
        global input
        global matrix
        global node
        node = []
        file = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', "Text files (*.txt)")
        if file:
            input = parsing.parse_adjacency_matrix(file[0])
            matrix = input.getMatrix()
            for i in range(len(input.getListNode())):
                node.append(input.getNameNode(i))

    
    # input start
    def input(self):
        global input
        input = self.start.text()
        print(input)

    #plot graph
    def plot_graph(self):
        Graph = nx.Graph()
        for nodes in Graph.nodes():
            Graph.nodes[nodes]['label'] = node[nodes]
        for i in range(len(node)):
            for j in range(i+1, len(node)):
                if matrix[i][j] != 0:
                    Graph.add_edge(node[i], node[j], weight=matrix[i][j])
        fig = Figure(figsize=(7,5), dpi=100)
        pos = nx.spring_layout(Graph)
        ax = fig.add_subplot(111)
        nx.draw(Graph, pos, with_labels=True, node_size=200, node_color='red', font_size=10, ax=ax)
        canvas = FigureCanvas(fig)
        path_color = 'green'
        nx.draw_networkx_edges(Graph, pos, edgelist=[(path[i], path[i+1]) for i in range(len(path)-1)], edge_color=path_color)
        nx.draw_networkx_edges(Graph, pos, edgelist=[(u, v) for (u, v) in Graph.edges() if (u, v) not in [(path[i], path[i+1]) for i in range(len(path)-1)]])
        plt.axis('off')
        canvas.setParent(self.widget)
        canvas.show()

    #ucs
    def chooseUCS(self):
        global cost
        global path
        cost, path = algorithm.uniform_cost_search(graph=input, start = self.start.text(), goal = self.goal.text())
        return cost, path

    #astar
    def chooseA(self):
        global cost
        global path
        cost, path = algorithm.a_star(graph=input, start = self.start.text(), goal = self.goal.text())
        return cost, path

    #dropdown
    def dropdownChanged(self):
        if self.dropdown.currentText() == "ITB":
            pass
        elif self.dropdown.currentText() == "Alun-Alun Bandung":
            pass
        elif self.dropdown.currentText() == "Bandung Selatan":
            pass
        elif self.dropdown.currentText() == "Jatinangor":
            pass
        elif self.dropdown.currentText() == "Input File":
            pass

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = UI()
    sys.exit(app.exec_())