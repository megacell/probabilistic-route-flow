import random

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

import route_flow.road_network
from route_flow import routers
import route_flow.routers.shortest_path_router

CMAP_NAME = 'winter'

def main():
    los_angeles_highways = route_flow.road_network.RoadNetwork.los_angeles(3)
    shortest_path_router = routers.shortest_path_router.ShortestPathRouter(
        los_angeles_highways, np.log(10))

    origin, destination = random.choice(
        los_angeles_highways.od_demand.od_pairs())
    print origin._taz_id, destination._taz_id

    route = shortest_path_router.route_for_od(origin, destination)
    node_pos_dict = {node:data['pos'] for node, data in
                     los_angeles_highways.network.nodes_iter(data=True)}
    nx.draw(route.network,
            node_pos_dict,
            cmap=plt.get_cmap(CMAP_NAME),
            vmin=0.0, vmax=1.0,
            node_color=[1.0 if node in route.path else 0.0
                        for node in route.network.nodes()],
            edge_cmap=plt.get_cmap(CMAP_NAME),
            edge_color=route.link_likelihood_list(),
            width=3.0, edge_vmin=0.0, edge_vmax=1.0,
            arrows=False, hold=True)
    nx.draw_networkx_edge_labels(
        route.network, node_pos_dict,
        edge_labels={k:("%3.2f"%v) for k,v in
                     route.link_likelihood().iteritems()},
        label_pos=0.3, hold=True)
    plt.show()

if __name__=='__main__':
    main()
