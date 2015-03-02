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

__author__ = "syadlowsky"

class BaseRouter(object):

    def __init__(self, road_network, beta=1.0):
        self._road_network = road_network
        self._beta = beta

    def path_for_od(self, r, s):
        pass

    def route_for_od(self, r, s):
        path = self.path_for_od(r, s)
        route = self._road_network.network.copy()

        # Set node weights
        for node in route:
            try:
                dist_from_path = min((nx.shortest_path_length(route, node, on_path)
                                      for on_path in path))
            except nx.NetworkXNoPath:
                dist_from_path = 0

            route.node[node]['weight'] = math.exp(-self._beta*dist_from_path)

        # Create policy from weights
        for node in route:
            edges = route.edges(node)
            total_edge_weight = reduce(
                lambda x,y: x+y,
                [route.node[v]['weight'] for u,v in edges],
                0.0)

            for u,v in edges:
                route[u][v]['weight'] = \
                    route.node[v]['weight'] / float(total_edge_weight)

        return route
