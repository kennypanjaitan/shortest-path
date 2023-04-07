import heapq
import Components as comp

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