import unittest
import random

import matplotlib.pyplot as plt
import networkx as nx
import cvxopt

from tests.test_factory import TestFactory

from route_flow.routers.equilibrium_router import EquilibriumRouter
from route_flow.origin import Origin
from route_flow.route import Route

__author__ = 'syadlowsky'

class TestEquilibriumRouter(unittest.TestCase):
    def setUp(self):
        if 'show_progress' in cvxopt.solvers.options:
            self._current_progress = cvxopt.solvers.options['show_progress']
        else:
            self._current_progress = True

        cvxopt.solvers.options['show_progress'] = False

        self.road_network = TestFactory.create_los_angeles_network()
        # TODO(syadlowsky): should be randomly selected
        self.od_pair = (Origin(8.0, [8.0]), Origin(22.0, [22.0]))
        self.subject = EquilibriumRouter(self.road_network)

    def tearDown(self):
        cvxopt.solvers.options['show_progress'] = self._current_progress

    def test_path_for_od(self):
        r, s = self.od_pair
        path = self.subject.path_for_od(r, s)
        self.assertEqual([8.0, 17.0, 36.0, 37.0, 38.0, 28.0, 22.0], path)

    # Should be a policy over links
    def test_route_for_od(self):
        r, s = self.od_pair
        route = self.subject.route_for_od(r, s)
        self.assertIsInstance(route, Route)

if __name__ == '__main__':
    unittest.main()
