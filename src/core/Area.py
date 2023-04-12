class Area:
    # ATRIBUTTES -----------------------------
    # center: tuple (x, y) center coordinate of the map
    # zoom: Int (zoom level)
    # listCoordinate: list of tuples [(x, y)] coordinate of nodes
    # listName: list of strings (name of nodes)
    # matrix: list of list of int (adjacency matrix)

    # CONSTRUCTOR ----------------------------
    def __init__(self, x, y, zoom, listCoordinate, listName, matrix):
        self.__center = (x, y)
        self.__zoom = zoom
        self.__listCoordinate = listCoordinate
        self.__listName = listName
        self.__matrix = matrix

    # GETTER ---------------------------------
    def getCenter(self):
        return self.__center
    
    def getZoom(self):
        return self.__zoom
    
    def getListCoordinate(self):
        return self.__listCoordinate
    
    def getListName(self):
        return self.__listName
    
    def getMatrix(self):
        return self.__matrix
    
