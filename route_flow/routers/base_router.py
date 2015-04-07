"""
This class generates routes for OD pairs in a road network.

REFERENCES
None
"""

# IMPORTS
import math

import networkx as nx
import scipy.io

from route_flow import road_network
from route_flow import routers
from route_flow.route import Route

__author__ = "syadlowsky"

class BaseRouter(object):

    def __init__(self, road_network, beta=1.0):
        self._road_network = road_network
        self._beta = beta

    def paths_for_od(self, r, s):
        """Returns an iterator over paths"""
        pass

    def path_for_od(self, r, s, **kwargs):
        return next(self.paths_for_od(r, s, **kwargs))

    @staticmethod
    def _edge_in_path(path, edge):
        u,v = edge
        if u in path:
            index = path.index(u)
            if index < len(path)-1:
                return v == path[index+1]

        return False

    def route_for_od(self, r, s):
        return next(self.routes_for_od(r, s))

    def routes_for_od(self, r, s):
        """Returns a generator for routes from paths created by paths_for_od"""

        for path in self.paths_for_od(r, s):
            route = self._road_network.network.copy()

            for edge in route.edges_iter():
                u,v = edge
                if BaseRouter._edge_in_path(path, edge):
                    route.edge[u][v]['pathweight'] = 0.1
                else:
                    route.edge[u][v]['pathweight'] = 1.0

            # Set node weights
            for node in route:
                try:
                    dist_from_path = nx.shortest_path_length(route,
                                                             node,
                                                             path[-1],
                                                             weight='pathweight')
                except nx.NetworkXNoPath:
                    dist_from_path = float('inf')

                route.node[node]['weight'] = math.exp(-self._beta*dist_from_path)

            
            # Create policy from weights
            def edge_weight(u,v):
                return route.node[v]['weight']*math.exp(
                    -self._beta*route.edge[u][v]['pathweight'])

            for node in route:
                edges = route.edges(node)
                total_edge_weight = reduce(
                    lambda x,y: x+y,
                    [edge_weight(u,v) for u,v in edges],
                    0.0)

                for u,v in edges:
                    route[u][v]['weight'] = \
                        edge_weight(u, v) / float(total_edge_weight)

            yield Route(route, path)
