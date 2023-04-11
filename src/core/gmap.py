import gmplot
import places.alunalun as nangor
import os
import webbrowser
import Components as comp
import function as func
import algorithm as algo
import Area as mp

# INITIATE MAP
place = mp.Place(nangor.x, nangor.y, nangor.zoom, nangor.listKoordinat, nangor.listNodeName, nangor.matriks)
gmap = gmplot.GoogleMapPlotter(place.getCenter()[0], place.getCenter()[1], place.getZoom())
for i in range(len(place.getListCoordinate())):
    for j in range(len(place.getListCoordinate())):
        if(nangor.matriks[i][j] == 1):
            latitude = [place.getListCoordinate()[i][0],place.getListCoordinate()[j][0]]
            longitude = [place.getListCoordinate()[i][1],place.getListCoordinate()[j][1]]
            gmap.scatter(latitude, longitude, 'yellow', size = 7, marker = False)
            gmap.plot(latitude, longitude, 'blue', edge_width = 3)

for k in range(len(place.getListCoordinate())):
    gmap.text(place.getListCoordinate()[k][0], place.getListCoordinate()[k][1], place.getListName()[k])

# ALGORITHM
nodeList = func.initiateListNode(nangor.listNodeName, nangor.matriks)
grafMap = comp.Graph(nangor.matriks, nodeList)
grafMap.convertCoordinatesToWAM(place.getListCoordinate())
algo.heuristicMap(grafMap, 'Patung Tentara Pelajar', place)
# cost, path = algo.uniform_cost_search(grafMap, 'Pungkur', 'Patung Tentara Pelajar')
cost, path = algo.a_star(grafMap, 'Pungkur', 'Patung Tentara Pelajar')
print(cost)
print(path)

# DRAW PATH
for i in range(len(path)-1):
    x = place.getListName().index(path[i])
    y = place.getListName().index(path[i+1])
    latitude = [place.getListCoordinate()[x][0],place.getListCoordinate()[y][0]]
    longitude = [place.getListCoordinate()[x][1],place.getListCoordinate()[y][1]]
    gmap.scatter(latitude, longitude, 'orange', size = 7, marker = True)
    gmap.plot(latitude, longitude, 'red', edge_width = 3)

gmap.draw("mymap.html")

webbrowser.open_new_tab('file://' + os.path.realpath('mymap.html'))