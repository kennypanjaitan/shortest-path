import Components

def parse_adjacency_matrix(file_path):
    global graf
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
        for i in range(len(nodeName)):
            name = nodeName[i]
            adjacent = adjacency_matrix[i]
            heuristic = 0
            node = Components.Node(name, adjacent, heuristic)
            nodeList.append(node)
    
    # initialize Graph
    graf = Components.Graph(adjacency_matrix, nodeList)
    return graf

def parse_adjacency_list(file_path):
    global graf
    nodeList = []                       # list of node
    nodeName = []                       # list of string (node name)
    adjacency_list = []                 # list of list of tuple (adjacency list)
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # return empty list if file is empty
    if len(lines) == 0 or '\n' not in lines:
        return adjacency_list, nodeName
    
    idxName = lines.index('\n')         # find '\n' to seperate list and node name
    if idxName != -1:
        
        # convert string to list of list of tuple (adjacency list)
        line = lines[:idxName]
        for l in line:
            adjacency_list.append([tuple(x.split(':')) for x in l.strip().split()])
        
        # return empty list if list is empty
        if len(adjacency_list) == 0:
            return [], []
        
        # convert string to list of string (node name)
        nodes = lines[idxName + 1:]
        for node in nodes:
            nodeName = node.strip().split()

        # return empty list if node name is empty or not equal to list size
        if len(nodeName) == 0 or len(nodeName) != len(adjacency_list):
            return [], []
        
        # convert list of string to list of node
        for i in range(len(nodeName)):
            name = nodeName[i]
            adjacent = adjacency_list[i]
            heuristic = 0
            node = Components.Node(name, adjacent, heuristic)
            nodeList.append(node)

    return adjacency_list