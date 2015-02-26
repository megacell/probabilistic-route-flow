import unittest
import random

from tests.test_factory import TestFactory

__author__ = 'syadlowsky'

class TestODDemand(unittest.TestCase):
    def setUp(self):
        myseed = 237423433
        random.seed(myseed)
        
        self._origins, self._od_demand_dictionary, self.subject = \
        TestFactory.create_od_demand()

    def test_find_by_od(self):
        test_origin = self._origins[0]
        test_destination = self._origins[0]
        self.assertEqual(
            self._od_demand_dictionary[test_origin][test_destination],
            self.subject.find_by_od(test_origin, test_destination))

    def test_find_by_od_no_such_destination(self):
        from route_flow.origin import Origin
        test_origin = self._origins[0]
        test_destination = Origin(999, [1, 2, 3])
        self.assertIsNone(
            self.subject.find_by_od(test_origin, test_destination))

if __name__ == '__main__':
    unittest.main()
