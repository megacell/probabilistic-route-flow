import unittest
import random

__author__ = 'syadlowsky'

class TestODDemand(unittest.TestCase):
    def setUp(self):
        from route_flow.od_demand import ODDemand

        myseed = 237423433
        random.seed(myseed)

        self._origins = self._create_origins()
        self._od_demand_dictionary = self._create_od_demand_dictionary(
            self._origins)

        self.subject = ODDemand(self._od_demand_dictionary)

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

    def _create_origins(self):
        from route_flow.origin import Origin
        origins = []
        for i in xrange(5):
            vertices = [random.randint(1, 10),
                        random.randint(10, 20),
                        random.randint(20, 30)]
            origin = Origin(i, vertices)
            origins.append(origin)
        return origins

    def _create_od_demand_dictionary(self, origins):
        od_demand = {}
        for r in origins:
            od_demand[r] = {}
            for s in origins:
                od_demand[r][s] = (r, s, random.uniform(0, 100))
        return od_demand

if __name__ == '__main__':
    unittest.main()
