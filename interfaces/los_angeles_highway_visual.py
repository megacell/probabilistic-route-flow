import networkx as nx
import matplotlib.pyplot as plt

import route_flow.road_network

def main():
    los_angeles_highways = route_flow.road_network.RoadNetwork.los_angeles(3)
    node_pos_dict = {node:data['pos'] for node, data in
                     los_angeles_highways.network.nodes_iter(data=True)}
    nx.draw(los_angeles_highways.network, node_pos_dict)
    plt.show()

if __name__=='__main__':
    main()
