class Node:
    # ATRIBUTTES -----------------------------
    # name: String
    # adjacents: List of Int (adjacency list)
    # heuristic: Int (heuristic value)
    # idx: Int (index of node in list of nodes)

    # CONSTRUCTOR ----------------------------
    def __init__(self, name, adjacents, heuristic):
        self.__name = name
        self.__adjacents = adjacents
        self.__heuristic = heuristic

    # GETTER ---------------------------------
    def getName(self):
        return self.__name
    
    def getAdjacents(self):
        return self.__adjacents
    
    def getHeuristic(self):
        return self.__heuristic
    
    def setHeuristic(self, heuristic):
        self.__heuristic = heuristic

    def getIdx(self):
        return self.__idx
    
    def getWeight(self, idx):
        return self.__adjacents[idx]
    
    # METHODS --------------------------------
    def __str__(self):
        adjacent_str = ''
        adjacent_node = ''
        for i in range(len(self.__adjacents)):
            adjacent_str += str(self.__adjacents[i]) + ' '
            if self.__adjacents[i] != 0:
                adjacent_node += str(i) + ' '

        return 'Name: ' + self.__name + '\nAdjacency List: ' + adjacent_str + '\nAdjacent Node: ' + adjacent_node + '\nHeuristic: ' + str(self.__heuristic) + '\n'


class Graph:
    # ATTRIBUTES -----------------------------
    # matrix: List of List of Int
    # nodes: List of Node

    # CONSTRUCTOR ----------------------------
    def __init__(self, matrix, nodes):
        self.__matrix = matrix
        self.__nodes = nodes

    # GETTER ---------------------------------
    def getMatrix(self):
        return self.__matrix
    
    def getListNode(self):
        return self.__nodes
    
    def getNode(self, name):
        for i in range(len(self.__nodes)):
            if self.__nodes[i].getName() == name:
                return self.__nodes[i]
        return None
    
    def getNodeIdx(self, idx):
        return self.__nodes[idx]
    
    def getIdxNode(self, node):
        for i in range(len(self.__nodes)):
            if self.__nodes[i] == node:
                return i
        return -1
    
    def getNeighbor(self, node):
        neighbor = []
        for i in range(len(self.__nodes)):
            if self.__matrix[self.getIdxNode(node)][i] != 0:
                neighbor.append(self.getNodeIdx(i))
        return neighbor
    
    def getNodeWeight(self, node1, node2):
        return self.__matrix[self.getIdxNode(node1)][self.getIdxNode(node2)]
    
    def getNameNode(self, idx):
        return self.__nodes[idx].getName()