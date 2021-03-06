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

class ODDemand(object):

    def __init__(self, od_demand_dictionary={}):
        # TODO(syadlowsky): document form of od_demand_dictionary
        self._lookup = od_demand_dictionary
        self._form_destination_lookup()

    def find_by_od(self, r, s):
        try:
            return self._lookup[r][s]
        except KeyError:
            return None

    def find_by_origin(self, r):
        try:
            return self._lookup[r].values()
        except KeyError:
            return None

    def find_by_destination(self, s):
        try:
            origins = self._destination_lookup[s]
        except KeyError:
            return None
        return (self.find_by_od(r, s) for r in origins)

    def od_pairs(self):
        """Lists OD pairs in network"""
        return [(r,s) for r, dests in
                    self._lookup.iteritems() for s in dests]

    @property
    def destinations(self):
        return self._destination_lookup.keys()

    @property
    def origins(self):
        return self._lookup.keys()

    def _form_destination_lookup(self):
        self._destination_lookup = {}
        for r, destination_demand_map in self._lookup.iteritems():
            for s in destination_demand_map.keys():
                if s in self._destination_lookup:
                    self._destination_lookup[s].append(r)
                else:
                    self._destination_lookup[s] = [r]

    def __str__(self):
        _str = "Origin   Dest Demand\n"
        for r in self.origins:
            for _, s, f in self.find_by_origin(r):
                _str += "%6i %6i %6.2f\n" % (r._taz_id, s._taz_id, f)
        return _str

    def __iter__(self):
        for r, dest_dict in self._lookup.iteritems():
            for s, d in dest_dict.iteritems():
                yield d

if __name__ == "__main__":
    # For reproducible results, set or save your seed to the random number
    # generator
    import sys
    myseed = random.randint(0, sys.maxint)
    # np.random.seed(myseed)  # If you're using numpy's random module
    random.seed(myseed)

    print "Random seed: %s" % g.seed
