"""
This is a class which keeps track of a route. In this work, a route is defined
as a policy over intersections in a network, where the most likely edge is
attempted to be taken, and with probbabilities associated with each edge, a
transition is stochastically taken. We present a formal correspondance between
a path (defined as an ordered list of nodes in a network) and a route (defined
as above).

Once this routing policy has been defined, the road network graph behaves like
a weighted random walk over a graph, ie. a Markov chain. See references for
theory behind how we calculate the link likelihood, P(visiting link | taking
route).

REFERENCES
http://www.springer.com/cda/content/document/cda_downloaddocument/9783642051555-c1.pdf?SGWID=0-0-45-834115-p173939734
"""

# IMPORTS
import networkx as nx
import numpy as np

from route_flow.util.memoize import memoize

# Then follows authorship information
__author__ = "syadlowsky"

class Route(object):

    def __init__(self, network, path):
        self.network = network
        self.path = path

    @memoize
    def link_likelihood(self):
        """Returns P(visiting link | taking this route)"""
        nodelist = self.network.nodes()
        nodelist.remove(self.path[-1])
        starting_entry = nodelist.index(self.path[0])

        Q = nx.adjacency_matrix(self.network, nodelist)
        I = np.eye(Q.shape[0])
        N = np.linalg.inv(I - Q)
        # TODO(syadlowsky): we only need one column or row of this, so don't
        # make whole thing.
        H = N.dot(np.linalg.inv(np.diag(np.diag(N))))

        chance_of_visit_node = np.squeeze(np.array(H[starting_entry, :])).tolist()

        likelihoods = {}
        for u, chance_of_visiting in zip(nodelist, chance_of_visit_node):
            for v in self.network[u]:
                likelihoods[(u, v)] = \
                    chance_of_visiting*self.network[u][v]['weight']

        return likelihoods

    def link_likelihood_list(self):
        likelihoods = self.link_likelihood()

        likelihood_list = []
        for e in self.network.edges_iter():
            if e in likelihoods:
                likelihood_list.append(likelihoods[e])
            else:
                likelihood_list.append(0.0)

        return likelihood_list

if __name__ == "__main__":
    # For reproducible results, set or save your seed to the random number
    # generator
    import sys
    myseed = random.randint(0, sys.maxint)
    # np.random.seed(myseed)  # If you're using numpy's random module
    random.seed(myseed)

    print "Random seed: %s" % g.seed
