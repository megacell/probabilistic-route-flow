#!/usr/bin/env python
"""
This is the simple class which defines the origins of a road network. These are
usually TAZ.

REFERENCES
None
"""

# IMPORTS

# Then follows authorship information
__author__ = "syadlowsky"

class Origin(object):

    def __init__(self, id_, vertices):
        self._vertices = vertices
        self._taz_id = id_

    def contains_vertex(self, vertex):
        return vertex in self._vertices

    def identified_as(self, id_):
        return self._taz_id == id_

    def __contains__(self, vertex):
        return self.contains_vertex(vertex)

if __name__ == "__main__":
    # For reproducible results, set or save your seed to the random number
    # generator
    import sys
    myseed = random.randint(0, sys.maxint)
    # np.random.seed(myseed)  # If you're using numpy's random module
    random.seed(myseed)

    print "Random seed: %s" % g.seed
