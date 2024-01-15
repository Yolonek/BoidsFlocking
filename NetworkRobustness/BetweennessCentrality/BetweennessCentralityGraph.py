from matplotlib import pyplot as plt
from CommonFunctions import read_json_file, make_directories, check_if_file_exists
import os


if __name__ == '__main__':
    samples = 500
    N = 500
    degrees = [2, 4]
    graph_type = 'BA'

    image_path = 'images'
    results_path = 'results'
    make_directories([results_path, image_path])

    degree_str = ''
    for deg in degrees:
        degree_str += f'k{deg}'
    file_title = f'BetweennessCentrality{graph_type}N{N}L{samples}deg{degree_str}.json'

    ba_dict = read_json_file(file_title, sub_dir=results_path)
    print(ba_dict)

    graph_type = 'WS'
    file_title = f'BetweennessCentrality{graph_type}N{N}L{samples}deg{degree_str}.json'

    ws_dict = read_json_file(file_title, sub_dir=results_path)
    print(ws_dict)

    degrees = [0.5, 1, 2, 4]
    graph_type = 'ERG'
    degree_str = ''
    for deg in degrees:
        degree_str += f'k{deg}'
    file_title = f'BetweennessCentrality{graph_type}N{N}L{samples}deg{degree_str}.json'

    erg_dict = read_json_file(file_title, sub_dir=results_path)
    print(erg_dict)

    figure, axes = plt.subplots(3, 1, layout='constrained', figsize=(8, 13))
    colors = ['green', 'maroon', 'blue', 'goldenrod', 'indigo']

    for index, data in enumerate([erg_dict, ba_dict, ws_dict]):
        graph = data['type']
        fspace = data['fspace']
        degrees = data['degrees']
        for color, degree in enumerate(degrees.keys()):
            component = degrees[degree][0]
            simtime = degrees[degree][1]
            label = f'$k = {degree}$, time: {round(simtime / 3600, 2)} h'
            axes[index].plot(fspace, component, label=label, color=colors[color])
        axes[index].legend()
        axes[index].set(xlim=[0, 1], ylim=[0, 1])
        axes[index].grid()

        ylabel = r'$\frac{P_{\infty}(f)}{P_{\infty}(0)}$'
        xlabel = '$f$'
        axes[index].set_xlabel(xlabel)
        axes[index].set_ylabel(ylabel, rotation=0, fontsize=16, labelpad=20)

        if graph == 'BA':
            graph = 'Barabasi-Albert'
        elif graph == 'ERG':
            graph = 'Random'
        else:
            graph = 'Watts-Strogatz'
        title = f'{graph} graph'
        axes[index].set_title(title)

    fig_title = f'Giant component size in function of fraction $f$ of graph removed.\n' \
                f'Betweenness Centrality\n' \
                f'Average: {samples} samples, Nodes: {N}'
    figure.suptitle(fig_title)

    file_name = f'BetweennessCentralityN{N}L{samples}.png'
    image_name = os.path.join(image_path, file_name)
    if not check_if_file_exists(image_name):
        figure.savefig(image_name)
    plt.show()
