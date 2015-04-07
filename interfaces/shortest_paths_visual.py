#!/usr/bin/env python
import random
import argparse
import itertools

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

import route_flow.road_network
from route_flow import routers
import route_flow.routers.shortest_path_router
import route_flow.routers.equilibrium_router
from route_flow.util.uniform_cost_traversal import uniform_cost

CMAP_NAME = 'PiYG'

def main():
    args = parse_args()

    los_angeles_highways = route_flow.road_network.RoadNetwork.los_angeles(
        args.demand)
    r, s = random.choice(
        los_angeles_highways.od_demand.od_pairs())

    shortest_path_router = routers.equilibrium_router.EquilibriumRouter(
        los_angeles_highways, np.log(10))

    routes = shortest_path_router.routes_for_od(r, s)
    route = routes.next()

    for route in itertools.islice(
            uniform_cost(route.network, r._taz_id, s._taz_id), 0, 10, 1):
        print route

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
