"""
This class generates shortest route paths according to equilibrium costs for OD
pairs in a road network.

REFERENCES
None
"""

# IMPORTS
import networkx as nx
import scipy.io

from route_flow import road_network
import route_flow.routers.base_router
from route_flow.routers.shortest_path_router import ShortestPathRouter
from route_flow.util.user_equilibrium_solver import UserEquilibriumSolver

__author__ = "syadlowsky"

class EquilibriumRouter(ShortestPathRouter):

    def __init__(self, road_network, beta=1.0):
        super(ShortestPathRouter, self).__init__(road_network, beta)

    def path_for_od(self, r, s):
        self._set_equilibrium_cost()

        return super(EquilibriumRouter, self).path_for_od(r, s, weight='ue_cost')

    def _set_equilibrium_cost(self):
        link_flow = UserEquilibriumSolver.equilibrium_link_flows(
            self._road_network)

        for i, (u,v) in enumerate(self._road_network.network.edges_iter()):
            self._road_network.network[u][v]['ue_cost'] = link_flow[i]
