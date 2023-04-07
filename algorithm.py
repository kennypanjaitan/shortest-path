import heapq

def uniform_cost_search(graph, listNode, start, goal):
    pqueue = [(0, (start, []))]
    explored = set()
    

    while pqueue:
        cost, (current, tempPath) = heapq.heappop(pqueue)
        print(current)
        if current == goal:
            return cost, (tempPath + [current])

        if current in explored:
            continue
        
        current_idx = listNode.index(current)
        explored.add(current)

        for neighbor_idx, neighbor_cost in enumerate(graph[current_idx]):
            if neighbor_cost == 0:
                continue

            new_cost = cost + neighbor_cost
            new_path = tempPath + [current]
            new_node = listNode[neighbor_idx]
            
            heapq.heappush(pqueue, (new_cost, (new_node, new_path)))

    return None