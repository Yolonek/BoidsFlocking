import networkx as nx
from GraphAnalyzer import GraphAnalyzer, AverageDegreeCalculator
from matplotlib import pyplot as plt
from CommonFunctions import make_directories, check_if_file_exists
import os


if __name__ == '__main__':
    N = 100
    deg = 30
    calculator = AverageDegreeCalculator(N=N, degree_to_get=deg)

    image_path = 'images'
    make_directories([image_path])

    L = calculator.parameter_from_er_degree()
    graph_type = 'ER'

    graph = GraphAnalyzer(graph_type, (N, L))
    graph.plot_graph(layout=nx.circular_layout)

    # calculating data
    graph.graph_degree_list()
    graph.average_degree_and_histogram()

    graph.calculate_clustering_coefficients()
    graph.calculate_average_coefficient()

    graph.calculate_path_histogram()
    graph.calculate_diameter_from_histogram()
    graph.calculate_average_path_from_histogram()

    fig = plt.gcf()
    title = f'{graph.graph_type} Graph. N = {N}, L = {L}\n' \
            f'average: degree = {graph.average_degree}, coefficient = {graph.average_coefficient}, ' \
            f'path length = {graph.average_path}'
    fig.suptitle(title, fontsize=20)
    fig.set_size_inches(14, 14)

    file_name = f'ERgraphN{N}deg{deg}.png'
    image_name = os.path.join(image_path, file_name)
    if not check_if_file_exists(image_name):
        fig.savefig(image_name)
    plt.show()

