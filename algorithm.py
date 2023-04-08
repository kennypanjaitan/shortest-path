import heapq
import Components as comp
import numpy as np

# Uniform cost search
def uniform_cost_search(graph: comp.Graph, start, goal):
    pqueue = [(0, (start, []))]     # queue of tuple(cost: int, (nodename: string, path: list of node name))
    explored = set()                # set of explored node
    
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
            new_node = graph.getNodeIdx(i).getName()
            
            heapq.heappush(pqueue, (new_cost, (new_node, new_path)))

    return 0, []

# A* search
def a_star(graph: comp.Graph, start, goal):
    pqueue = [(0, (start, []))]     # queue of tuple(cost: int, (nodename: string, path: list of node name))
    explored = set()                # set of explored node
    cameFrom = {}                   # dictionary of node and its parent

    # count g(n)
    g = [float ('inf') for i in range(len(graph.getListNode()))]
    g[graph.getIdxNode(start)] = 0

    # count f(n)
    f = [float ('inf') for i in range(len(graph.getListNode()))]
    f[graph.getIdxNode(start)] = graph.getNodeWeight(start, goal)

    setHash = {start}

    while (pqueue):
        cost, (current, tempPath) = heapq.heappop(pqueue)

        # check if current node is goal
        if current == goal:
            return cost, tempPath

        # check if current node is explored
        if current in explored:
            continue
        
        # add current node to explored set
        explored.add(current)

        # add adjacent node to queue
        for neighbor in graph.getNeighbor(current):
            temp_g = g[graph.getIdxNode(current)] + graph.getNodeWeight(current, neighbor)
            if temp_g < g[graph.getIdxNode(neighbor)]:
                cameFrom[neighbor] = graph.getIdxNode(current)
                g[graph.getIdxNode(neighbor)] = temp_g
                f[graph.getIdxNode(neighbor)] = temp_g + graph.getNodeWeight(neighbor, goal)
                if neighbor not in setHash:
                    setHash.add(neighbor)
                    heapq.heappush(pqueue, (f[graph.getIdxNode(neighbor)], (neighbor, tempPath + [current])))
    
    return cost, tempPath