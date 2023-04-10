import Components as comp
import function as func

def parse_adjacency_matrix(file_path):
    nodeList = []                       # list of node
    nodeName = []                       # list of string (node name)
    adjacency_matrix = []               # matrix of int (adjacency matrix)
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # return empty matrix if file is empty
    if len(lines) == 0 or '\n' not in lines:
        return adjacency_matrix, nodeName
    
    idxName = lines.index('\n')         # find '\n' to seperate matrix and node name
    if idxName != -1:
        
        # convert string to list of list of int (adjacency matrix)
        line = lines[:idxName]
        for l in line:
            adjacency_matrix.append([int(x) for x in l.strip().split()])
        
        # return empty matrix if matrix is empty or not square
        if len(adjacency_matrix) == 0 or len(adjacency_matrix[0]) == 0 or len(adjacency_matrix) != len(adjacency_matrix[0]):
            return [], []
        
        # convert string to list of string (node name)
        nodes = lines[idxName + 1:]
        for node in nodes:
            nodeName = node.strip().split()

        # return empty matrix if node name is empty or not equal to matrix size
        if len(nodeName) == 0 or len(nodeName) != len(adjacency_matrix):
            return [], []
        
        # convert list of string to list of node
        nodeList = func.initiateListNode(nodeName, adjacency_matrix)
    
    # initialize Graph
    graf = comp.Graph(adjacency_matrix, nodeList)
    return graf