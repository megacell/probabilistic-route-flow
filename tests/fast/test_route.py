import unittest
import random

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from tests.test_factory import TestFactory

from route_flow.route import Route
from route_flow.road_network import RoadNetwork
from route_flow.routers.base_router import BaseRouter

__author__ = 'syadlowsky'

class TestRoute(unittest.TestCase):
    def setUp(self):
        self.graph = nx.house_graph().to_directed()
        self.path = [3, 4]
        self.road_network = RoadNetwork(self.graph, None)
        router = BaseRouter(self.road_network, beta=np.log(10))
        router.path_for_od = lambda r,s: self.path

        route = router.route_for_od(3,4)
        self.subject = Route(router.route_for_od(3,4), self.path)

    def test_link_likelihood(self):
        ll = {
            (0, 1) : 0.0014151*0.5,
            (0, 2) : 0.0014151*0.5,
            (1, 0) : 0.0871639/101,
            (1, 3) : 8.71639/101,
            (2, 0) : 0.0913201/201,
            (2, 3) : 9.13201/201,
            (2, 4) : 9.13201/201,
            (3, 1) : 1.0/12,
            (3, 2) : 1.0/12,
            (3, 4) : 10.0/12
        }
        for k,v in self.subject.link_likelihood().iteritems():
            self.assertAlmostEqual(ll[k], v, places=5,
                                   msg="Not equal for edge %s: %s, %s" %
                                   (str(k),v,ll[k]))

if __name__ == '__main__':
    unittest.main()
