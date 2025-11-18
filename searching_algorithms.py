import making_a_maze
from collections import deque
from queue import PriorityQueue

def DFS(graph, current_node, looked_at=[], came_from={}): 
    looked_at.append(current_node)
    neighbours = graph[current_node]

    for neighbour in neighbours:
        if neighbour not in looked_at:
            came_from[neighbour] = current_node
            DFS(graph, current_node=neighbour)
            
    return looked_at, came_from

def BFS(graph, current_nodes, looked_at=[], came_from={}):
    if not current_nodes:
        return

    current_node = current_nodes.popleft()
    looked_at.append(current_node)
    
    neighbours = graph[current_node]

    for neighbour in neighbours:
        if neighbour not in looked_at:
            current_nodes.append(neighbour)
            came_from[neighbour] = current_node

    BFS(graph, current_nodes)
    return looked_at, came_from




