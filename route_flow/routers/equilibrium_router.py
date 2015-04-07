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
        self._costs_calculated = False
        super(ShortestPathRouter, self).__init__(road_network, beta)

    def paths_for_od(self, r, s):
        self._set_equilibrium_cost()

        return super(EquilibriumRouter, self).paths_for_od(
            r, s, weight='ue_cost')

    def _set_equilibrium_cost(self):
        if self._costs_calculated:
            return
        
        link_flow = UserEquilibriumSolver.equilibrium_link_flows(
            self._road_network)

        for i, (u,v) in enumerate(self._road_network.network.edges_iter()):
            edge = self._road_network.network[u][v]

            free_flow_delay = edge['free_flow_delay']
            delay_slope = edge['delay_slope']

            cost = free_flow_delay * (1 + 0.15*(link_flow[i] * delay_slope)**4)

            self._road_network.network[u][v]['ue_cost'] = round(cost, 2)

        self._costs_calculated = True
