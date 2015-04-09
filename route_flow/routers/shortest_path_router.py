"""
This class generates shortest route paths for OD pairs in a road network.

REFERENCES
None
"""

# IMPORTS
import networkx as nx
import scipy.io
import numpy as np

from route_flow import road_network
from route_flow.util.uniform_cost_traversal import uniform_cost
from route_flow.util.all_shortest_paths import all_shortest_paths
import route_flow.routers.base_router

__author__ = "syadlowsky"

class ShortestPathRouter(route_flow.routers.base_router.BaseRouter):

    def __init__(self, road_network, beta=1.0):
        super(ShortestPathRouter, self).__init__(road_network, beta)

    def paths_for_od(self, r, s, weight='free_flow_delay'):
        start_node = r.vertices[0]
        end_node = s.vertices[0]
        paths = self._shortest_paths(start_node, end_node, weight=weight)
        return paths

    def _shortest_paths(self, start_node, end_node, weight=None):
        path_cost_so_far = float('inf')
        for cost, path in all_shortest_paths(self._road_network.network,
                                       start_node, end_node, weight):
            if cost > path_cost_so_far and not np.isclose(cost,
                                                          path_cost_so_far,
                                                          rtol = 0.005):
                break
            yield path
            path_cost_so_far = cost
