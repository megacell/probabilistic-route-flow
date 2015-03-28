"""
This class generates shortest route paths for OD pairs in a road network.

REFERENCES
None
"""

# IMPORTS
import networkx as nx
import scipy.io

from route_flow import road_network
import route_flow.routers.base_router

__author__ = "syadlowsky"

class ShortestPathRouter(route_flow.routers.base_router.BaseRouter):

    def __init__(self, road_network, beta=1.0):
        super(ShortestPathRouter, self).__init__(road_network, beta)

    def paths_for_od(self, r, s, weight='free_flow_delay'):
        start_node = r.vertices[0]
        end_node = s.vertices[0]
        return nx.all_shortest_paths(self._road_network.network, start_node,
                                end_node, weight=weight)
