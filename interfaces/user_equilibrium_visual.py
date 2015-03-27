#!/usr/bin/env python
import random

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pickle

import route_flow.road_network
from route_flow import routers
from route_flow.util.user_equilibrium_solver import UserEquilibriumSolver
import route_flow.routers.shortest_path_router

CMAP_NAME = 'PiYG'

def main():
    los_angeles_highways = route_flow.road_network.RoadNetwork.los_angeles()

    link_flows = UserEquilibriumSolver.equilibrium_link_flows(
        los_angeles_highways)
    pickle.dump(link_flows, open('link_flows.pkl', 'w'))
    # link_flows = pickle.load(open('link_flows.pkl'))

    node_pos_dict = {node:data['pos'] for node, data in
                     los_angeles_highways.network.nodes_iter(data=True)}

    edges = los_angeles_highways.network.edges()

    nx.draw(los_angeles_highways.network,
            node_pos_dict,
            #edge_cmap=plt.get_cmap(CMAP_NAME),
            #edge_color={(edges[k]):v for k,v in
            #         enumerate(link_flows)},
            width=3.0, edge_vmin=link_flows.min(), edge_vmax=link_flows.max(),
            arrows=False, hold=True)
    nx.draw_networkx_edge_labels(
        los_angeles_highways.network, node_pos_dict,
        edge_labels={(edges[k]):("%3.2f"%v) for k,v in
                     enumerate(link_flows)},
        label_pos=0.3, hold=True)
    plt.show()

if __name__=='__main__':
    main()
