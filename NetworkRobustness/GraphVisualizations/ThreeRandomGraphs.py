import networkx as nx
from matplotlib import pyplot as plt
from GraphAnalyzer import GraphAnalyzer, AverageDegreeCalculator
from CommonFunctions import make_directories, check_if_file_exists
import os


if __name__ == '__main__':
    N = 100
    deg = 30
    beta = 0.3

    image_path = 'images'
    make_directories([image_path])

    calculator = AverageDegreeCalculator(N=N, degree_to_get=deg)

    L = calculator.parameter_from_er_degree()
    p = calculator.parameter_from_erg_degree()
    k = calculator.parameter_from_ws_degree()

    er_graph = GraphAnalyzer('ER', (N, L))
    erg_graph = GraphAnalyzer('ERG', (N, p))
    ws_graph = GraphAnalyzer('WS', (N, k, beta))
    graph_list = [er_graph, erg_graph, ws_graph]

    for graph in graph_list:
        graph.graph_degree_list()
        graph.average_degree_and_histogram()

        graph.calculate_clustering_coefficients()
        graph.calculate_average_coefficient()

        graph.calculate_path_histogram()
        graph.calculate_diameter_from_histogram()
        graph.calculate_average_path_from_histogram()

    figure, axis = plt.subplots(3, 1, layout='constrained', figsize=(9, 15))
    colors = ['maroon', 'green', 'blue']

    title_er = f'{er_graph.graph_type} Graph. N = {N}, L = {L}\n'
    title_erg = f'{er_graph.graph_type} Graph. N = {N}, p = {p}\n'
    title_ws = f'{er_graph.graph_type} Graph. N = {N}, k = {k}, beta = {beta}\n'
    title_list = [title_er, title_erg, title_ws]

    for graph, index in zip(graph_list, range(3)):
        graph.plot_graph(layout=nx.kamada_kawai_layout, node_color=colors[index],
                         node_size=50, ax=axis[index])
        title_end = f'average: degree = {graph.average_degree}, ' \
                    f'coefficient = {graph.average_coefficient}, ' \
                    f'path length = {graph.average_path}'
        axis[index].set_title(title_list[index] + title_end)

    figure.suptitle(f'Three random graphs for {N} nodes and degree {deg}.')

    file_name = f'RandomGraphsN{N}deg{deg}.png'
    image_name = os.path.join(image_path, file_name)
    if not check_if_file_exists(image_name):
        figure.savefig(image_name)
    plt.show()
