from PyQt5.QtWidgets import QMainWindow, QApplication, QGraphicsView, QGraphicsEllipseItem, QGraphicsScene, QGraphicsRectItem, QPushButton, QFileDialog, QComboBox, QLineEdit, QGraphicsLineItem
from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QRectF
from PyQt5 import uic
import sys
sys.path.append('../src/')
import algorithm
import Components as comp
import parsing

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

        # start
        self.start = self.findChild(QLineEdit, "lineEdit")
        
        # goal
        self.goal = self.findChild(QLineEdit, "lineEdit_2")

        self.show()
    
        
    # input file
    def pushInputFile(self):
        global input
        global matrix
        file = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', "Text files (*.txt)")
        if file:
            input = parsing.parse_adjacency_matrix(file[0])
            matrix = input.getMatrix()
 
    
    # input start
    def input(self):
        global input
        input = self.start.text()
        print(input)

    def plot_graph(self):
        scene = QGraphicsScene()
        scene.setSceneRect(QRectF(510,180,701,431))
        node_size = 10
        for i in range (len(matrix)):
            node = QGraphicsEllipseItem(0,0,node_size,node_size)
            node.setBrush(QBrush(QColor(255,0,0)))
            node.setPen(QPen(QColor(0,0,0)))
            node.setPos((i+1)*100,100)
            scene.addItem(node)
        for i in range (len(matrix)):
            for j in range (len(matrix[i])):
                if matrix[i][j] != 0:
                    line = QGraphicsLineItem((i+1)*100+5,100+5,(j+1)*100+5,100+5)
                    line.setPen(QPen(QColor(0,0,0)))
                    scene.addItem(line)
        self.view = QGraphicsView()
        self.view.setScene(scene)
        self.view.show()

    #ucs
    def chooseUCS(self):
        cost, path = algorithm.uniform_cost_search(graph=input, start = self.start.text(), goal = self.goal.text())
        print(cost)
        print(path)

    #astar
    def chooseA(self):
        cost, path = algorithm.a_star(graph=input, start = self.start.text(), goal = self.goal.text())
        print(cost)
        print(path)

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
        

app = QApplication(sys.argv)
window = UI()
app.exec_()