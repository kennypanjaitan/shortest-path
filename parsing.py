import Components

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

        # convert string to list of string (node name)
        nodes = lines[idxName + 1:]
        for node in nodes:
            nodeName = node.strip().split()

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

