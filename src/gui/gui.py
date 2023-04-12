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
from src.places import itbBdg as gane, itbNangor as nangor, alunalun as alun, cilacap as cilacap, buahBatu as batu


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
        self.dropdown.addItems(["Input File", "ITB Ganesha", "ITB Jatinangor", "Alun-Alun Bandung", "Buah Batu", "Cilacap"])
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
        
        # showmap
        self.map = self.findChild(QPushButton, "pushButton_5")
        self.map.clicked.connect(self.showmap)
        self.widget2 = QWidget(self)

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

            elif self.dropdown.currentText() == "Buah Batu":
                place = area.Area(batu.x, batu.y, batu.zoom, batu.listKoordinat, batu.listNodeName, batu.matriks)
                
            elif self.dropdown.currentText() == "Cilacap":
                place = area.Area(cilacap.x, cilacap.y, cilacap.zoom, cilacap.listKoordinat, cilacap.listNodeName, cilacap.matriks)

            self.initiateMapToGraph(place)
                
    #show map
    def showmap(self):
        if self.dropdown.currentText() == "ITB Ganesha":
            self.widget2 = QWidget()
            self.widget2.resize(800, 600)
            label = QLabel(self.widget2)
            Gane = "ITB Ganesha\n 1. Gerbang Utama\n 2. Gedung Sipil\n 3. Gedung CIBE\n 4. CC Barat\n 5. CC Timur\n 6. Lapangan Cinta\n 7. Gedung SAPPK\n 8. Gedung SR \n 9. Sekretariat IMG\n 10. Gedung Lingkungan\n 11. GKU Barat\n 12. Labtek VII\n 13. Labtek III\n 14. Gedung Kimia\n 15. Gedung FTTM\n 16. Gedung FITB\n 17. Gedung CAS\n 18. Gedung CRCS\n 19. Perpustakaan\n 20. Gedung SBM\n 21. Sunken Court\n 22. Pusat Gema\n 23. Plaza Widya\n 24. Aula Barat-Timur"
            label.setText(str(Gane))
            self.widget2.setWindowTitle("ITB Ganesha")
            self.widget2.show()
        elif self.dropdown.currentText() == "ITB Jatinangor":
            self.widget2 = QWidget()
            self.widget2.resize(500, 300)
            label = QLabel(self.widget2)
            Nangor = "ITB Jatinangor\n 1. Gerbang Utama\n 2. Bundaran\n 3. GKU\n 4. Water Treatment Plan\n 5. Asrama Mahasiswa\n 6. GSG\n 7. Koica\n 8. Rektorat\n 9. GKU 1\n 10. Asrama Dosen"
            label.setText(str(Nangor))
            self.widget2.setWindowTitle("ITB Jatinangor")
            self.widget2.show()
        elif self.dropdown.currentText() == "Alun-Alun Bandung":
            self.widget2 = QWidget()
            self.widget2.resize(800, 600)
            label = QLabel(self.widget2)
            Alun = "Alun-Alun Bandung\n 1. Paskal\n 2. Parapan Kebon Jati\n 3. Sudirman\n 4. Stasiun Bandung\n 5. Cibadak\n 6. Astana Anyar\n 7. Pasir Koja\n 8. Norsefiicden\n 9. Otto Iskandar Dinata\n 10. Pungkur\n 11. Patung Tentara Pelajar\n 12. Braga Citywalk\n 13. Braga\n 14. Air Mancur Asia Afrika\n 15. Jalan ABC\n 16. Asia Afrika\n 17. Mural Asia Afrika\n 18. Jalan Homan\n 19. Alun-Alun Bandung\n 20. Pendopo Kota Bandung\n 21. Pasar Baru"
            label.setText(str(Alun))
            self.widget2.setWindowTitle("Alun-Alun Bandung")
            self.widget2.show()
        elif self.dropdown.currentText() == "Buah Batu":
            self. widget2 = QWidget()
            self.widget2.resize(800, 600)
            label = QLabel(self.widget2)
            Batu = "Buah batu\n 1. Jalan Neptunus Barat II - III\n 2. Jalan Neptunus Barat III - V\n 3. Jalan Neptunus Barat IV - Neptunus Raya Barat\n 4. Jalan Neptunus Barat VI - Neptunus Raya Barat\n 5. Jalan Neptunus Barat III - Neptunus Raya Barat\n 6. Jalan Neptunus Barat II - Neptunus Raya Barat - Neptunus Tengah\n 6. Jalan Neptunus Barat I - Neptunus Barat - Neptunus Raya\n 7. Jalan Neptunus Tengah II - Neptunus Tengah"
            label.setText(str(Batu))
            self.widget2.setWindowTitle("Buah Batu")
            self.widget2.show()
        elif self.dropdown.currentText() == "Cilacap":
            self.widget2 = QWidget()
            self.widget2.resize(500, 300)
            label = QLabel(self.widget2)
            Cilacap = "Cilacap\n 1. Pelabuhan Penyebrangan Sleko\n 2. Pelabuhan Internasional Tanjung Intan\n 3. Cilacap Town Square\n 4. Stasiun Cilacap\n 5. Pendopo Wijaya Kusuma Sakti\n 6. Masjid Agung Darussalam\n 7. Soedirman Soccer Field\n 8. Tugu Nelayan\n 9. Klenteng Lam Tjeng Kiong"
            label.setText(str(Cilacap))
            self.widget2.setWindowTitle("Cilacap")
            self.widget2.show()
        elif self.dropdown.currentText() == "Input File":
            self.widget2 = QWidget()
            self.widget2.resize(100,100)
            label = QLabel(self.widget2)
            label.setText("You Choose Input File")
            self.widget2.setWindowTitle("Input File")
            self.widget2.show()

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
            path_font = QFont()
            path_font.setPointSize(8)
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
            if self.dropdown.currentText() == "Input File":
                algo.heuristic(self.graphUI, self.goal.text())
            else:
                algo.heuristicMap(self.graphUI, self.goal.text(), place)
                
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

def initiateUI():
    app = QApplication(sys.argv)
    window = UI()
    sys.exit(app.exec_())

if __name__ == '__main__':
    # import sys
    app = QApplication(sys.argv)
    window = UI()
    sys.exit(app.exec_())
