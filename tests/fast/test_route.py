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

        self.subject = router.route_for_od(3,4)

    def test_link_likelihood(self):
        # WARNING: fragile test
        # TODO(syadlowsky): make less fragile
        ll = {(0, 1): 8.531394237142512e-05,
              (3, 2): 0.012311154324422098,
              (1, 3): 0.009740393156933971,
              (3, 1): 0.009779097481936406,
              (2, 4): 0.006928163741619479,
              (2, 0): 6.928163741619475e-05,
              (2, 3): 0.005503236074761374,
              (1, 0): 0.0001226242846613018,
              (3, 4): 0.9779097481936414,
              (0, 2): 0.00010740389003173026}
        for k,v in self.subject.link_likelihood().iteritems():
            self.assertAlmostEqual(ll[k], v, places=5,
                                   msg="Not equal for edge %s: %s, %s" %
                                   (str(k),v,ll[k]))

if __name__ == '__main__':
    unittest.main()
