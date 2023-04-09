import Components as comp
import numpy as np

# Initiate list of node
# /* listNodeName: list of string (node name)
#    adjacentyMatrix: list of list of int (adjacency matrix)
#    return: list of Node 
# */
def initiateListNode(listNodeName, adjacentyMatrix):
    listNode = []                               # list of node
    for i in range(len(listNodeName)):          # iterate through list of node name to iniate list of Node
        name = listNodeName[i]
        adjacentList = adjacentyMatrix[i]
        node = comp.Node(name, adjacentList)
        listNode.append(node)

    return listNode


# Count euclidean distance between two points
# euclidean distance is for 2D plane
def euclideanDistance(x1, y1, x2, y2):
    return np.sqrt(np.square(x1 - x2) + np.square(y1 - y2))


# Count haversine distance between two points
# /* haversine distance is for earth surface (sphere)
#    lat and lon are in degrees
#    return: approximate distance in kilometers
# */
def haversineDistance(lat1, lon1, lat2, lon2):
    R = 6372.8 # Earth radius in kilometers

    # convert lat and lon difference to radians
    dLat = np.radians(lat2 - lat1)
    dLon = np.radians(lon2 - lon1)

    # convert lat to radians
    lat1 = np.radians(lat1)
    lat2 = np.radians(lat2)

    # haversine formula
    a = np.sin(dLat/2)**2 + np.sin(dLon/2)**2 * np.cos(lat1) * np.cos(lat2)
    c = 2 * np.arcsin(np.sqrt(a))

    # calculate final approximate distance in kilometers
    return R * c