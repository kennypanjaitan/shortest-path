import heapq
import Components as comp
import numpy as np

# UNIFORM COST SEARCH =====================================================================
def uniform_cost_search(graph: comp.Graph, start, goal):
    pqueue = [(0, (start, []))]     # queue of tuple (cost: int, (nodename: string, path: list of node name))
    explored = set()                # set of string (explored node)
    
    while pqueue:
        cost, (current, tempPath) = heapq.heappop(pqueue)

        # check if current node is goal
        if current == goal:
            return cost, (tempPath + [current])

        # check if current node is explored
        if current in explored:
            continue
        
        # add current node to explored set
        explored.add(current)

        # add adjacent node to queue
        currentNode = graph.getNode(current)
        for i in range(len(currentNode.getAdjacents())):
            # check if node is a neighbor
            if currentNode.getAdjacents()[i] == 0:
                continue

            new_cost = cost + currentNode.getAdjacents()[i]
            new_path = tempPath + [current]
            new_node = graph.getNodeByIdx(i).getName()
            
            heapq.heappush(pqueue, (new_cost, (new_node, new_path)))

    return 0, []


# A* SEARCH =================================================================================
# Heuristic Function
# /* 
#    h(n) = edge(s) covered to goal node 
#    Covering all node using BFS
# */
def heuristic(graph: comp.Graph, goal: str):
    explored = set()                # set of string (explored node)
    value = 0                       # int (distance to goal (edge(s) covered))
    queueNode = [(goal, value)]     # queue of string (node name)
    explored.add(goal)

    while queueNode:
        current, value = queueNode.pop(0)
        currentNode = graph.getNode(current)
        currentNode.setHeuristic(value)

        # add adjacent node to queue
        for i in range(len(currentNode.getAdjacents())):
            if currentNode.getAdjacents()[i] > 0 and graph.getNodeByIdx(i).getName() not in explored:
                neighbor = graph.getNodeByIdx(i).getName()
                queueNode.append((neighbor, value + 1))
                explored.add(neighbor)
    

# Main Algorithm
def a_star(graph: comp.Graph, start: str, goal: str):
    heuristic(graph, goal)                                                  # set heuristic value for each node

    pqueue = [(0 + graph.getNode(start).getHeuristic(), (start, 0, []))]    # queue of tuple (f(n): int, (nodename: string, g(n): int, path: list of node name))
    explored = set()                                                        # set of string (explored node)
    
    while pqueue:
        fValue, (current, cost, tempPath) = heapq.heappop(pqueue)

        # check if current node is goal
        if current == goal:
            return cost, (tempPath + [current])

        # check if current node is explored
        if current in explored:
            continue
        
        # add current node to explored set
        explored.add(current)

        # add adjacent node to queue
        currentNode = graph.getNode(current)
        for i in range(len(currentNode.getAdjacents())):
            # check if node is a neighbor
            if currentNode.getAdjacents()[i] == 0:
                continue

            new_cost    = cost + currentNode.getAdjacents()[i]
            new_fValue  = new_cost + graph.getNodeByIdx(i).getHeuristic()
            new_path    = tempPath + [current]
            new_node    = graph.getNodeByIdx(i).getName()
            
            heapq.heappush(pqueue, (new_fValue, (new_node, new_cost, new_path)))

    return 0, []