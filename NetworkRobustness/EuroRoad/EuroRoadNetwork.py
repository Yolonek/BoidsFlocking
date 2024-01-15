import networkx as nx
from matplotlib import pyplot as plt
from CommonFunctions import read_tuple_data


if __name__ == '__main__':
    path = 'euroroad.txt'

    with open(path, 'r') as file:
        nodes = file.readlines()

    nodes = list(map(read_tuple_data, nodes))

    road_graph = nx.Graph()
    road_graph.add_edges_from(nodes)

    figure, axes = plt.subplots(3, 1, layout='constrained', figsize=(9, 15))

    layouts = (nx.random_layout, nx.kamada_kawai_layout, nx.spiral_layout)
    colors = ('maroon', 'green', 'blue')
    for ax, layout, color in zip(figure.axes, layouts, colors):
        nx.draw(road_graph, pos=layout(road_graph), ax=ax,
                node_color=color, alpha=0.3, node_size=50)

    axes[0].set_title('Random Layout')
    axes[1].set_title('Kamada-Kawai Layout')
    axes[2].set_title('Spiral Layout')

    figure.suptitle('Graph of Euro-roadmap for three different layouts')
    plt.show()
    figure.savefig('EuroRoadmap.png')