import unittest
import random

__author__ = 'syadlowsky'

class TestOrigin(unittest.TestCase):
    def setUp(self):
        from route_flow.origin import Origin 
        # The setup code is run before each test
        myseed = 237423433
        random.seed(myseed)
        self.origin_id = random.randint(0, 10)
        self.vertices = [random.randint(1, 10),
                         random.randint(10, 20),
                         random.randint(20, 30)]
        self.subject = Origin(self.origin_id,
                              self.vertices)

    def test_contains_vertex(self):
        self.assertTrue(self.subject.contains_vertex(self.vertices[0]))
        self.assertFalse(self.subject.contains_vertex(0))

    def test_identified_as(self):
        self.assertTrue(self.subject.identified_as(self.origin_id))
        self.assertFalse(self.subject.identified_as(self.origin_id + 1))

if __name__ == '__main__':
    unittest.main()
