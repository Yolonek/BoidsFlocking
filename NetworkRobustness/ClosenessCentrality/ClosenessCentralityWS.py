from GraphAnalyzer import GraphAnalyzer, AverageDegreeCalculator
import numpy as np
from time import time
from CommonFunctions import save_json_file, make_directories


if __name__ == '__main__':
    samples = 500
    N = 500
    degrees = [2, 4]
    graph_type = 'WS'
    beta = 0.01

    f_space = np.linspace(0, 1, 101)

    data_dict = {'type': graph_type,
                 'N': N,
                 'samples': samples,
                 'fspace': f_space.tolist(),
                 'degrees': {}}

    calculator = AverageDegreeCalculator(N=N)

    results_path = 'results'
    make_directories([results_path])

    t_total = 0
    for degree in degrees:
        t1 = time()

        calculator.change_degree(degree)
        k = calculator.parameter_from_ws_degree()

        graph = GraphAnalyzer(graph_type, (N, k, beta))
        graph.assign_initial_n()

        avg_component = np.zeros(len(f_space))

        for index, f in enumerate(f_space):
            print(f)
            avg = 0
            for i in range(samples):
                graph.remove_fraction_of_nodes(f, centrality='closeness')
                avg += graph.calculate_giant_component()
                graph.create_graph(graph_type, (N, k, beta))

            avg_component[index] = avg / samples
        avg_component = avg_component / graph.initial_N

        t2 = time()
        delta = round(t2 - t1)
        print(f'Degree: {degree}, time taken: {delta} seconds')
        t_total += delta

        data_dict['degrees'][str(degree)] = (avg_component.tolist(), delta)

    print(f'Done. Total time: {t_total} seconds')

    degree_str = ''
    for deg in degrees:
        degree_str += f'k{deg}'
    file_title = f'ClosenessCentrality{graph_type}N{N}L{samples}deg{degree_str}.json'

    save_json_file(data_dict, file_title, sub_dir=results_path)
