"""
This is a class which stores information about OD demands for a given road
network. Conceptually, one should imagine this stores tuples of the form
(origin [Origin], destination [Origin], demand [float]) where the primary
key is (origin, destination).

REFERENCES
None
"""

# IMPORTS

# Then follows authorship information
__author__ = "syadlowsky"

class RoadNetwork:

    def __init__(self, network, od_demand):
        self.network = network
        self._od_demand = od_demand
