"""
This is a class which stores information about OD demands for a given road
network. Conceptually, one should imagine this stores tuples of the form
(origin [Origin], destination [Origin], demand [float]) where the primary
key is (origin, destination).

REFERENCES
None
"""

# IMPORTS
import networkx as nx
import scipy.io

import od_demand
import origin

# Then follows authorship information
__author__ = "syadlowsky"

class RoadNetwork:

    def __init__(self, network, od_demand):
        self.network = network
        self.od_demand = od_demand

    @classmethod
    def los_angeles(_class, demand=3, parameters=None, path=None):
        """Generate small map of L.A. with 122 links and 44 modes
        """

        if not path:
            path = 'data/los_angeles_data_2.mat'
        data = scipy.io.loadmat(path)

        nodes = data['nodes']
        links = data['links']

        if demand in [1, 2, 3, 4]:
            ODs = data["ODs%d" % demand]
        else:
            raise Exception("No such demand")

        # TODO(syadlowsky): probably should be MultiDiGraph, but for now, this
        # is good enough. No networks we work with have two links between same
        # intersections.
        network = nx.DiGraph()
        od_demand_dict = {}

        for index, (posx, posy) in enumerate(nodes):
            network.add_node(index, pos=(posx, posy))

        for startnode, endnode, route, ffdelay, slope in links:
            if startnode < 1:
                print "HAHA"
            network.add_edge(startnode, endnode, free_flow_delay=ffdelay,
                             delay_slope=slope)

        for (r, s, flow) in ODs:
            origin_ = origin.Origin(r, [r])
            destination = origin.Origin(s, [s])
            if origin not in od_demand_dict:
                od_demand_dict[origin_] = {}
            od_demand_dict[origin_][destination] = (origin_, destination, flow)

        return RoadNetwork(network, od_demand.ODDemand(od_demand_dict))
