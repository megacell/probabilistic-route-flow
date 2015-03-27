import cvxopt
import networkx as nx
import pickle

import numpy as np

from route_flow.util.kktsolver import get_kktsolver

class UserEquilibriumSolver(object):

    @classmethod
    def equilibrium_link_flows(_class, road_network):
        n_edges = nx.number_of_edges(road_network.network)
        n_destinations = len(road_network.od_demand.destinations)
        A, b = _class.flow_conservation_constraints(road_network)
        G, h = _class.non_negativity_contraints(road_network)
        F = _class.rosenthal_objective(road_network)

        dims = {'l': G.size[0], 'q': [], 's': []}
        kktsolver = get_kktsolver(G, dims, A, F)

        x = cvxopt.solvers.cp(F, G=G, h=h, A=A, b=b,
                              kktsolver=kktsolver)['x']

        n_destinations = len(road_network.od_demand.destinations)
        n_edges = nx.number_of_edges(road_network.network)

        linkflows = cvxopt.matrix(0.0, (n_edges,1))
        for destination_index in range(n_destinations):
            offset = destination_index * n_edges
            linkflows += x[offset:offset + n_edges]

        return np.array(linkflows)

    @classmethod
    def non_negativity_contraints(_class, road_network):
        n_edges = nx.number_of_edges(road_network.network)
        n_destinations = len(road_network.od_demand.destinations)
        G = -cvxopt.spdiag(cvxopt.matrix([1 for i in xrange(n_destinations*n_edges)]))
        h = cvxopt.matrix(0.0, (n_destinations*n_edges,1))
        return (G, h)

    @classmethod
    def demand_vector(_class, road_network):
        n_nodes = nx.number_of_nodes(road_network.network)
        node_lookup = {e:i for i, e in enumerate(road_network.network.nodes())}
        destinations = road_network.od_demand.destinations
        n_destinations = len(destinations)

        signed_demand = cvxopt.matrix(0.0, (n_nodes * n_destinations, 1),
                                      tc='d')

        for i, s in enumerate(destinations):
            offset = n_nodes * i
            nodes_in_destination = [offset + node_lookup[e] for e in s.vertices]
            destination_split_ratio = len(nodes_in_destination)
            for r, _, demand in road_network.od_demand.find_by_destination(s):
                nodes_in_origin = [offset + node_lookup[e] for e in r.vertices]
                origin_split_ratio = len(nodes_in_origin)

                signed_demand[nodes_in_destination] += demand
                signed_demand[nodes_in_origin] -= demand

        return signed_demand

    @classmethod
    def destinationwise_incidence_matrix(_class, road_network):
        n_edges = nx.number_of_edges(road_network.network)
        n_nodes = nx.number_of_nodes(road_network.network)
        n_destinations = len(road_network.od_demand.destinations)

        A = cvxopt.spmatrix([], [], [], (n_destinations * n_nodes,
                                         n_destinations * n_edges), tc='d')
        incidence = nx.incidence_matrix(road_network.network, oriented=True)

        for destination_index in xrange(n_destinations):
            node_offset = destination_index * n_nodes
            edge_offset = destination_index * n_edges
            A[node_offset:node_offset + n_nodes,
              edge_offset:edge_offset + n_edges] = incidence

        return A

    @classmethod
    def flow_conservation_constraints(_class, road_network):
        A = _class.destinationwise_incidence_matrix(road_network)
        b = cvxopt.matrix(_class.demand_vector(road_network))

        return (A, b)

    @classmethod
    def cost_function(_class, free_flow_delay, flow, delay_slope):
        """Computes the BPR cost function.

        Input parameters should be cvxopt matrices.

        Computes the following BPR link delay function:
        S_a \left( {v_a } \right) = t_a \left( {1 + 0.15\left( {\frac{{v_a }}
        {{c_a }}} \right)^4 } \right)
        t_a = free flow travel time on link a per unit of time
        v_a = volume of traffic on link a per unit of time (somewhat more
              accurately: flow attempting to use link a).
        c_a = capacity of link a per unit of time
        S_a(v_a) is the average travel time for a vehicle on link a
        """

        congestion_factor = 0.15 * (cvxopt.mul(flow, delay_slope) ** 4)
        delay_with_flow = sum(cvxopt.mul((1 + congestion_factor),
                                         free_flow_delay))

        grad_delay_wrt_flow = cvxopt.mul(
            cvxopt.mul(0.6 * (cvxopt.mul(flow, delay_slope) ** 3), delay_slope),
            free_flow_delay)


        hessian_delay_wrt_flow = cvxopt.mul(
            cvxopt.mul(1.2 * (cvxopt.mul(flow, delay_slope) ** 2), delay_slope ** 2),
            free_flow_delay).T

        return (delay_with_flow, grad_delay_wrt_flow, hessian_delay_wrt_flow)

    @classmethod
    def objective_poly(_class, x, z, n_edges, n_destinations, free_flow_delay,
                       delay_slope, P, w_gap=1.0):
        """Objective function of UE program with polynomial delay functions
        f(x) = sum_i f_i(l_i)
        f_i(u) = sum_{k=1}^degree ks[i,k] u^k
        with l = sum_w x_w
        
        Parameters
        ----------
        x,z: variables for the F(x,z) function for cvxopt.solvers.cp
        ks: matrix of size (n,degree) 
        p: number of w's
        """

        # In this case, return tuple (number of nonlinear constraints, x_0 \in
        # \dom(f_0))
        if x is None:
            return (0, cvxopt.matrix(1.0/n_destinations,
                                     (n_destinations*n_edges,1)))

        # l is the total flow on each link. It is computed from the
        # destination-wise link flows.
        l = P * x

        f, Df, H = _class.cost_function(free_flow_delay, l, delay_slope)

        f *= w_gap
        Df *= w_gap
        H *= w_gap
        
        Df = cvxopt.matrix([[Df.T]]*n_destinations)
        if z is None:
            return f, Df
        return f, Df, cvxopt.matrix([[cvxopt.spdiag(z[0] * H)]*n_destinations]*n_destinations)

    @classmethod
    def rosenthal_objective(_class, road_network):
        n_edges = nx.number_of_edges(road_network.network)
        n_destinations = len(road_network.od_demand.destinations)
        free_flow_delay = cvxopt.matrix(
            [edge[2]['free_flow_delay'] for edge in
             road_network.network.edges_iter(data='free_flow_delay')],
            (n_edges, 1))
        delay_slope = cvxopt.matrix(
            [edge[2]['delay_slope'] for edge in
             road_network.network.edges_iter(data='delay_slope')],
            (n_edges, 1))

        P = cvxopt.matrix([[cvxopt.spdiag([1]*n_edges)]]*n_destinations)

        def F(x=None, z=None):
            return _class.objective_poly(x, z, n_edges, n_destinations,
                                         free_flow_delay, delay_slope, P)

        return F
