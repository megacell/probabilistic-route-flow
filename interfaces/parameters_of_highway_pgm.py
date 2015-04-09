#!/usr/bin/env python
import random
import argparse
import ipdb

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

import route_flow.road_network
from route_flow.origin import Origin
from route_flow import routers
import route_flow.routers.shortest_path_router
import route_flow.routers.equilibrium_router

CMAP_NAME = 'PiYG'

class ObservationLayer(object):
    def __init__(self):
        self._routes = []

    def add_route(self, route):
        self._routes.append(route)

    def link_route_likelihood_matrix(self):
        list_form = [route.link_likelihood_list() for route in self._routes]
        return np.array(list_form).T

    def get_markov_blanket_size(self, route):
        likelihood_list = np.array(route.link_likelihood_list())
        M = self.link_route_likelihood_matrix()

        child_locs = np.where(likelihood_list > 0.01)[0]
        routes_with_same_links = np.sum(M[child_locs,:] > 0.01, axis=1)

        return np.count_nonzero(routes_with_same_links)

def main():
    args = parse_args()

    los_angeles_highways = route_flow.road_network.RoadNetwork.los_angeles(
        args.demand)

    if args.router == 'shortest':
        router = routers.shortest_path_router.ShortestPathRouter(
            los_angeles_highways, np.log(10))
    elif args.router == 'equilibrium':
        router = routers.equilibrium_router.EquilibriumRouter(
            los_angeles_highways, np.log(10))

    origin, destination = random.choice(
        los_angeles_highways.od_demand.od_pairs())
#    origin = Origin(5.0, (5.0,))
#    destination = Origin(9.0, (9.0,))
    print "Origin:", origin._taz_id, "Destination:", destination._taz_id

    routes = tuple(router.routes_for_od(origin, destination))

    print "There are", len(routes), "routes between these ODs"

    def links_on_route(route):
        likelihood_dict = route.link_likelihood()
        
        return sum([1 for p in likelihood_dict.values() if p > 0.01])

    print "Average links per route:", np.mean(
        [links_on_route(r) for r in routes])

    print "Average base path length:", np.mean(
        [len(r.path) for r in routes])

    print "Links in network:", nx.number_of_edges(
        los_angeles_highways.network)

    observation_layer = ObservationLayer()
    n_routes = []
    for r, s, d in los_angeles_highways.od_demand:
        routes_for_od = list(router.routes_for_od(r, s))
        n_routes.append(len(routes_for_od))
        for route in routes_for_od:
            observation_layer.add_route(route)
    print "Average of", np.mean(n_routes), "shortest paths per OD pair"

    blanket_size = []
    for r, s, d in los_angeles_highways.od_demand:
        routes_for_od = list(router.routes_for_od(r, s))
        n_routes.append(len(routes_for_od))
        for route in routes_for_od:
            blanket_size.append(
                observation_layer.get_markov_blanket_size(route))
    print "Average Markov blanket size of", np.mean(blanket_size), "routes"
    print "Maximum Markov blanket size of", max(blanket_size), "routes"

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--router', type=str,
                        help="Which router to use (shortest, equilibrium).",
                        default='shortest')
    parser.add_argument('--demand', type=int,
                        help='Which demand profile to use (1 - 4).', default=4)
    args = parser.parse_args()
    return args

if __name__=='__main__':
    main()
