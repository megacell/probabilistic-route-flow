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

    def __init__(self, road_network):
        super(ShortestPathRouter, self).__init__(road_network)

    def path_for_od(self, r, s):
        # TODO(syadlowsky): shouldn't be accessing this private object. Need to
        # create an interface here.
        start_node = r._vertices[0]
        end_node = s._vertices[0]
        return nx.shortest_path(self._road_network.network, start_node,
                                end_node, weight='free_flow_delay')
