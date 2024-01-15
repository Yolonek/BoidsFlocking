import networkx as nx
from GraphAnalyzer import GraphAnalyzer
from CommonFunctions import read_tuple_data
from matplotlib import pyplot as plt
from time import time


if __name__ == '__main__':
    path = 'facebook_combined.txt'

    time_start = time()

    with open(path, 'r') as file:
        nodes = file.readlines()

    nodes = list(map(read_tuple_data, nodes))
    time_stop = time()
    delta = round(time_stop - time_start, 3)
    print(f'Nodes loaded, time: {delta} seconds...')

    time_start = time()
    facebook_graph = nx.Graph()
    facebook_graph.add_edges_from(nodes)

    fb_graph_analyzer = GraphAnalyzer(model_name='custom',
                                      model_parameters='Ego-Facebook',
                                      initial_graph=facebook_graph)
    time_stop = time()
    delta = round(time_stop - time_start, 3)
    print(f'Graph created, time: {delta} seconds...')

    # fb_graph_analyzer.plot_graph()
    # plt.show()

    # calculating all parameters
    time_start = time()
    sim_time_start = time()
    fb_graph_analyzer.graph_degree_list()
    fb_graph_analyzer.average_degree_and_histogram()
    time_stop = time()
    delta = round(time_stop - time_start, 3)
    print(f'Degree histogram calculated, time: {delta} seconds...')

    time_start = time()
    fb_graph_analyzer.calculate_clustering_coefficients()
    fb_graph_analyzer.calculate_average_coefficient()
    fb_graph_analyzer.calculate_coefficient_histogram()
    time_stop = time()
    delta = round(time_stop - time_start, 3)
    print(f'Clustering coefficient histogram calculated, time: {delta} seconds...')

    time_start = time()
    fb_graph_analyzer.calculate_path_histogram()
    fb_graph_analyzer.calculate_diameter_from_histogram()
    fb_graph_analyzer.calculate_average_path_from_histogram()
    time_stop = time()
    delta = round(time_stop - time_start, 3)
    print(f'Path histogram calculated, time: {delta} seconds...')
    sim_time_stop = time()
    sim_time = int(sim_time_stop - sim_time_start)

    # creating plots
    figure, axis = plt.subplots(3, 1, layout='constrained', figsize=(9, 15))
    colors = ('maroon', 'green', 'blue')

    # plot 1
    title = f'Degree distribution P(k),\naverage degree = {round(fb_graph_analyzer.average_degree, 3)}.'
    x_axis = fb_graph_analyzer.degree_histogram.keys()
    y_axis = fb_graph_analyzer.degree_histogram.values()
    axis[0].bar(x_axis, y_axis, color=colors[0])
    axis[0].set(title=title, xlabel='node degree', ylabel='node degree quantity', xlim=[0, 250])

    # plot 2
    title = f'Distribution of clustering coefficients,\n' \
            f'average coefficient = {fb_graph_analyzer.average_coefficient}'
    x_axis = fb_graph_analyzer.coefficient_histogram.keys()
    y_axis = fb_graph_analyzer.coefficient_histogram.values()
    axis[1].scatter(x_axis, y_axis, color=colors[1], marker='+')
    axis[1].set(title=title, xlabel='clustering coefficient', ylabel='coefficient quantity')
    axis[1].grid()

    # plot 3
    title = f'Distribution of shortest paths,\ndiameter = {fb_graph_analyzer.diameter},' \
            f' average path = {fb_graph_analyzer.average_path}'
    x_axis = fb_graph_analyzer.path_histogram.keys()
    y_axis = fb_graph_analyzer.path_histogram.values()
    axis[2].bar(x_axis, y_axis, color=colors[2])
    axis[2].set(title=title, xlabel='path length', ylabel='path quantity')

    title = f'Graph of ego-Facebook dataset. Calculation time: {sim_time} seconds,\n' \
            f'number of: nodes: {fb_graph_analyzer.N}, edges: {fb_graph_analyzer.graph.number_of_edges()}'
    figure.suptitle(title)
    # figure.savefig('EgoFacebook.png')
    plt.show()