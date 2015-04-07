#!/usr/bin/env python
import random
import argparse
import ipdb

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

import route_flow.road_network
from route_flow import routers
import route_flow.routers.shortest_path_router
import route_flow.routers.equilibrium_router

CMAP_NAME = 'PiYG'

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
    print "Origin:", origin._taz_id, "Destination:", destination._taz_id

    routes = tuple(router.routes_for_od(origin, destination))
    print routes

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
