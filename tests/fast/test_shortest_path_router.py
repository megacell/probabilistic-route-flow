import unittest
import random

import matplotlib.pyplot as plt
import networkx as nx

from tests.test_factory import TestFactory

from route_flow.routers.shortest_path_router import ShortestPathRouter
from route_flow.origin import Origin

__author__ = 'syadlowsky'

class TestShortestPathRouter(unittest.TestCase):
    def setUp(self):
        self.road_network = TestFactory.create_los_angeles_network()
        # TODO(syadlowsky): should be randomly selected
        self.od_pair = (Origin(8.0, [8.0]), Origin(22.0, [22.0]))
        self.subject = ShortestPathRouter(self.road_network)

    def test_path_for_od(self):
        r, s = self.od_pair
        path = self.subject.path_for_od(r, s)
        self.assertEqual([8.0, 17.0, 24.0, 37.0, 23.0, 22.0], path)

if __name__ == '__main__':
    unittest.main()
