def parse_adjacency_matrix(file_path):
    nodeName = []
    adjacency_matrix = []
    with open(file_path, 'r') as f:
        lines = f.readlines()

    idxName = lines.index('\n')
    if idxName != -1:
        line = lines[:idxName]
        for l in line:
            adjacency_matrix.append([int(x) for x in l.strip().split()])

        nodes = lines[idxName + 1:]
        for node in nodes:
            nodeName.append(node.strip().split())

    return adjacency_matrix, nodeName

matrix, nodeName = parse_adjacency_matrix('test.txt')

for i in range(len(matrix)):
    print(matrix[i])
    
for i in range(len(nodeName)):
    print(nodeName[i])