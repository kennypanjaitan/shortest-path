import itbNangor as nangor
import parsing
import algorithm as algo

# Parsing
graph = parsing.parse_adjacency_matrix('test.txt')

# UCS
cost, path = algo.uniform_cost_search(graph, 'A', 'C')

print(cost)
print(path)



