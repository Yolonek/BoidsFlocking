import networkx as nx
from GraphAnalyzer import GraphAnalyzer, AverageDegreeCalculator
from matplotlib import pyplot as plt
from CommonFunctions import make_directories, check_if_file_exists
import os


if __name__ == '__main__':
    N = 100
    deg = 2
    calculator = AverageDegreeCalculator(N=N, degree_to_get=deg)

    image_path = 'images'
    make_directories([image_path])

    m_2, m_1 = calculator.parameter_from_ba_degree()
    print(m_2, m_1)
    graph_type = 'BA'

    graph_1 = GraphAnalyzer(graph_type, (N, m_1))
    graph_2 = GraphAnalyzer(graph_type, (N, m_2))

    for graph in [graph_1, graph_2]:
        graph.graph_degree_list()
        graph.average_degree_and_histogram()

        graph.calculate_clustering_coefficients()
        graph.calculate_average_coefficient()

        graph.calculate_path_histogram()
        graph.calculate_diameter_from_histogram()
        graph.calculate_average_path_from_histogram()

    figure, axes = plt.subplots(2, 1, layout='constrained', figsize=(8, 14))
    colors = ['maroon', 'mediumblue']

    title_1 = f'{graph_1.graph_type} Graph. N = {N}, m = {m_1}\n'
    title_2 = f'{graph_2.graph_type} Graph. N = {N}, m = {m_2}\n'
    title_list = [title_1, title_2]

    for index, graph in enumerate([graph_1, graph_2]):
        graph.plot_graph(layout=nx.kamada_kawai_layout, node_color=colors[index],
                         node_size=50, ax=axes[index])
        title_end = f'average: degree = {graph.average_degree}, ' \
                    f'coefficient = {graph.average_coefficient}, ' \
                    f'path length = {graph.average_path}'
        axes[index].set_title(title_list[index] + title_end)

    figure.suptitle(f'Two random graphs for {N} nodes and degree {deg}.')

    file_name = f'BAgrapgN{N}.png'
    image_name = os.path.join(image_path, file_name)
    if not check_if_file_exists(image_name):
        figure.savefig(image_name)
    plt.show()