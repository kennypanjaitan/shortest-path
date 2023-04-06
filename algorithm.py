import heapq

def uniform_cost_search(graph, start, goal):
    pqueue = [(0, (start, []))]
    explored = set()
    

    while pqueue:
        cost, (current, tempPath) = heapq.heappop(pqueue)
        if current == goal:
            return cost, (tempPath + [current])

        if current in explored:
            continue

        explored.add(current)

        for neighbor, neighbor_cost in enumerate(graph[current]):
            if neighbor_cost == 0:
                continue

            new_cost = cost + neighbor_cost
            new_path = tempPath + [current]

            heapq.heappush(pqueue, (new_cost, (neighbor, new_path)))

    return None