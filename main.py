# import gmplot
import itbNangor as nangor
import parsing
import algorithm as algo

# Parsing
matrix, nodeName = parsing.parse_adjacency_matrix('test.txt')

# UCS
cost, path = algo.uniform_cost_search(matrix, nodeName, 'A', 'B')

print(cost)
print(path)



