import networkx as nx
from collections import defaultdict, deque

import Queue

def uniform_cost(G, source, dest, weight='ue_cost', reverse=False):
    """Produce edges in a breadth-first-search starting at source.

    Parameters
    ----------
    G : NetworkX graph

    source : node
       Specify starting node for breadth-first search and return edges in
       the component reachable from source.

    reverse : bool, optional
       If True traverse a directed graph in the reverse direction

    Returns
    -------
    edges: generator
       A generator of edges in the breadth-first-search.
    """
    if reverse and isinstance(G, nx.DiGraph):
        neighbors = G.predecessors_iter
    else:
        neighbors = G.neighbors_iter

    queue = Queue.PriorityQueue()
    queue.put((0, [source], neighbors(source)))
    while not queue.empty():
        cost, path, children = queue.get()
        parent = path[-1]
        if parent == dest:
            yield cost, path
        while True:
            try:
                child = next(children)
                child_cost = cost + G[parent][child][weight]
                child_path = path + [child]
                queue.put((child_cost, child_path, neighbors(child)))
            except StopIteration:
                break
