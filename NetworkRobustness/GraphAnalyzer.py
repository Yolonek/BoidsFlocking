import networkx as nx
import numpy as np
from networkx.exception import NetworkXError, NodeNotFound, NetworkXNoPath
from matplotlib import pyplot as plt
from math import sqrt


class ErdosRenyiGraphGenerator(object):
    def __init__(self, p=0.5, N=1):
        self.N = N
        self.p = p
        self.initial_grid = None
        self.current_grid = None
        self.link_list = None
        self.graph = nx.Graph()

    def set_initial_grid(self, initial_grid=None):
        if initial_grid is None:
            self.initial_grid = np.triu(np.random.random((self.N, self.N)), k=1)
        else:
            self.initial_grid = np.triu(initial_grid, 1)

    def grid_thresholding(self):
        self.current_grid = np.where(self.initial_grid < 1 - self.p, 0, 1).astype(int)

    def print_grid(self, initial=True):
        with np.printoptions(precision=3):
            if initial:
                print(self.initial_grid + np.eye(self.N))
            else:
                print(self.current_grid + np.eye(self.N, dtype=int))

    def convert_grid_to_link_tuple_(self):
        self.link_list = []
        link_cords = np.where(self.current_grid == 1)
        x_cords = link_cords[0]
        y_cords = link_cords[1]
        for x, y in zip(x_cords, y_cords):
            link_tuple = (int(x), int(y))
            self.link_list.append(link_tuple)

    def convert_grid_to_link_tuple(self):
        x_cords, y_cords = np.where(self.current_grid == 1)
        self.link_list = np.concatenate((x_cords[:, None], y_cords[:, None]), axis=1)

    def create_graph(self):
        self.graph.add_nodes_from(range(self.N))
        self.graph.add_edges_from(self.link_list)

    def generate_all_graph_data(self, initial_grid=None):
        self.set_initial_grid(initial_grid=initial_grid)
        self.grid_thresholding()
        self.convert_grid_to_link_tuple()
        self.create_graph()

    def get_nodes_and_links(self):
        return self.N, self.link_list

    def get_generated_graph(self):
        return self.graph


class GraphAnalyzer(object):
    def __init__(self, model_name, model_parameters, initial_graph=None):
        self.graph = None
        self.graph_type = None
        self.initial_graph = None
        self.initial_N = None
        self.N = None
        self.m = None
        self.L = None
        self.p = None
        self.k = None
        self.create_graph(model_name, model_parameters,
                          initial_graph=initial_graph)

        self.graph_degrees = None
        self.degree_histogram = {}
        self.average_degree = 0

        self.coefficient_dict = {}
        self.average_coefficient = 0
        self.coefficient_histogram = {}

        self.diameter = 0
        self.average_path = 0
        self.path_histogram = {}

    def plot_graph(self, layout=None, node_color='maroon', node_size=50, ax=None):
        pos = layout(self.graph) if layout else None
        nx.draw(self.graph, pos=pos, ax=ax, node_color=node_color, node_size=node_size, alpha=0.5)

    def create_graph(self, model_name, model_parameters, initial_graph=None):
        self.N = model_parameters[0]
        if model_name == 'ER':
            self.graph_type = 'Erdos-Renyi'
            self.L = model_parameters[1]
            if initial_graph:
                self.graph = initial_graph
            else:
                self.graph = nx.gnm_random_graph(self.N, self.L)
        elif model_name == 'ERG':
            self.graph_type = 'Erdos-Renyi-Gilbert'
            self.p = model_parameters[1]
            if initial_graph:
                self.graph = initial_graph
            else:
                self.graph = nx.erdos_renyi_graph(self.N, self.p)
        elif model_name == 'WS':
            self.graph_type = 'Watts-Strogatz'
            self.k = model_parameters[1]
            self.p = model_parameters[2]
            if initial_graph:
                self.graph = initial_graph
            else:
                self.graph = nx.watts_strogatz_graph(self.N, self.k, self.p)
        elif model_name == 'BA':
            self.graph_type = 'Barabasi-Albert'
            self.m = model_parameters[1]
            if initial_graph:
                self.graph = initial_graph
            else:
                self.graph = nx.barabasi_albert_graph(self.N, self.m)
        elif model_name == 'custom':
            self.graph_type = model_parameters
            self.N = initial_graph.number_of_nodes()
            self.graph = initial_graph

    def graph_degree_list(self):
        self.graph_degrees = list(self.graph.degree)

    def assign_initial_n(self):
        self.initial_N = self.N

    def update_n(self):
        self.N = len(self.graph.nodes)

    def calculate_centrality(self, centrality_type=None):
        if centrality_type:
            centrality_nodes = centrality_type(self.graph)
            centrality_nodes = sorted(centrality_nodes.items(),
                                      key=lambda x: x[1],
                                      reverse=True)
            return centrality_nodes
        return None

    def remove_listed_nodes(self, list_of_nodes):
        if self.graph:
            self.graph.remove_nodes_from(list_of_nodes)

    def remove_nth_node(self, N):
        if self.graph:
            self.graph.remove_node(N)

    def remove_fraction_of_nodes(self, fraction, centrality='random'):
        number_to_remove = round(self.N * fraction)
        list_of_nodes_to_remove = []
        if centrality == 'random':
            list_of_nodes_to_remove = np.random.choice(self.graph.nodes,
                                                       size=number_to_remove,
                                                       replace=False)
        elif centrality == 'degree':
            nodes = self.calculate_centrality(centrality_type=nx.degree_centrality)
            nodes = list(map(lambda x: x[0], nodes))
            list_of_nodes_to_remove = nodes[0:number_to_remove]
        elif centrality == 'closeness':
            nodes = self.calculate_centrality(centrality_type=nx.closeness_centrality)
            nodes = list(map(lambda x: x[0], nodes))
            list_of_nodes_to_remove = nodes[0:number_to_remove]
        elif centrality == 'betweenness':
            nodes = self.calculate_centrality(centrality_type=nx.betweenness_centrality)
            nodes = list(map(lambda x: x[0], nodes))
            list_of_nodes_to_remove = nodes[0:number_to_remove]

        self.remove_listed_nodes(list_of_nodes_to_remove)

    def calculate_giant_component(self):
        try:
            giant_component = len(max(nx.connected_components(self.graph), key=len))
        except ValueError:
            giant_component = 0
        return giant_component

    def average_degree_and_histogram(self, clear=True):
        if self.graph_degrees is None:
            self.graph_degree_list()
        if clear:
            self.degree_histogram = {}
            self.average_degree = 0
        for degree_tuple in self.graph_degrees:
            node_degree = degree_tuple[1]
            self.average_degree += node_degree

            if node_degree in self.degree_histogram.keys():
                self.degree_histogram[node_degree] += 1
            else:
                self.degree_histogram[node_degree] = 1
        self.average_degree = self.average_degree / self.N

    def calculate_clustering_coefficients(self):
        self.coefficient_dict = nx.clustering(self.graph)

    def calculate_average_coefficient(self):
        self.average_coefficient = round(sum(self.coefficient_dict.values()) / self.N, 3)

    def calculate_coefficient_histogram(self, clear=True):
        if clear:
            self.coefficient_histogram = {}
            self.calculate_clustering_coefficients()
        for coefficient in self.coefficient_dict.values():
            node_coefficient = round(coefficient, 3)
            if node_coefficient in self.coefficient_histogram.keys():
                self.coefficient_histogram[node_coefficient] += 1
            else:
                self.coefficient_histogram[node_coefficient] = 1

    def calculate_graph_diameter_nx(self):
        try:
            self.diameter = nx.diameter(self.graph)
        except NetworkXError:
            self.diameter = -1

    def calculate_average_shortest_path_nx(self):
        try:
            self.average_path = round(nx.average_shortest_path_length(self.graph), 3)
        except NetworkXError:
            self.average_path = -1

    def calculate_path_histogram(self, clear=True):
        if clear:
            self.path_histogram = {}
        for source in range(self.N):
            for target in range(source + 1, self.N):
                try:
                    path = nx.shortest_path_length(self.graph, source=source, target=target)
                    if path in self.path_histogram.keys():
                        self.path_histogram[path] += 1
                    else:
                        self.path_histogram[path] = 1
                except NetworkXNoPath:
                    pass

    def calculate_diameter_from_histogram(self):
        self.diameter = max(self.path_histogram.keys())

    def calculate_average_path_from_histogram(self):
        average_path = 0
        for path_length, path_quantity in self.path_histogram.items():
            average_path += path_length * path_quantity
        all_paths = sum(self.path_histogram.values())
        self.average_path = round(average_path / all_paths, 3)


class AverageDegreeCalculator(object):
    def __init__(self, N=10, degree_to_get=1):
        self.N = N
        self.degree = degree_to_get

    def change_degree(self, new_degree):
        self.degree = new_degree

    def change_number_of_nodes(self, N):
        self.N = N

    def parameter_from_er_degree(self):
        return int(self.degree * self.N / 2)

    def parameter_from_erg_degree(self):
        return round(self.degree / self.N, 3)

    def parameter_from_ws_degree(self):
        return self.degree

    def parameter_from_ba_degree(self):
        a = 2 / self.N
        b = (1 / (self.N * 2 ** 4)) - 2
        c = self.degree
        delta = b ** 2 - 4 * a * c
        x_1 = round((-b + sqrt(delta)) / (2 * a))
        x_2 = round((-b - sqrt(delta)) / (2 * a))
        return x_1, x_2


if __name__ == '__main__':
    graph = ErdosRenyiGraphGenerator(N=10)
    graph.set_initial_grid()
    graph.print_grid()
    graph.grid_thresholding()
    graph.print_grid(initial=False)
    graph.convert_grid_to_link_tuple_()
    print(graph.link_list)
    graph.convert_grid_to_link_tuple()
    print(graph.link_list)
    print(graph.link_list[0])
    graph.generate_all_graph_data()
    print(type(graph.graph.degree))