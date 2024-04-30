from helpers import Rectangle
from brute_force import BruteForceAlgorithm
from map import MapAlgorithm
from persistent_segment_tree import PersistentTreeAlgorithm
import matplotlib.pyplot as plt
from time import perf_counter

N = 100
REPEAT = 100
P_X = 1259
P_Y = 1567

ALGORITHMS = {
    "Brute force": BruteForceAlgorithm,
    "Map": MapAlgorithm,
    "Persistent segment tree": PersistentTreeAlgorithm
}


def test_rectangles(n):
    rectangles = []
    for i in range(n):
        rectangles.append(Rectangle(10 * i, 10 * i, 10 * (2 * N - i), 10 * (2 * N - i)))
    return rectangles


def test_queries(n):
    queries = []
    for i in range(n):
        queries.append(((P_X * i) ** 31 % (20 * N), (P_Y * i) ** 31 % (20 * N)))
    return queries


def draw_graph(results, values, title, log):
    if log:
        plt.xscale('log'), plt.yscale('log')
    for label, data in results.items():
        plt.plot(values, data, label=label)
    plt.title(title)
    plt.xlabel("Number of rectangles and queries")
    plt.ylabel("Time, seconds")
    plt.legend()
    plt.show()


def result_format(result):
    return '{0:.7f}'.format(result)


def test(p):
    values = [2 ** i for i in range(p)]
    preparation_dict = dict()
    query_dict = dict()
    for label, algorithm_cls in ALGORITHMS.items():
        preparation_dict[label] = []
        query_dict[label] = []
        for n in values:
            tmp_prep = []
            tmp_quer = []
            for _ in range(REPEAT):
                rectangles = test_rectangles(n)
                queries = test_queries(n)
                algorithm = algorithm_cls()
                start = perf_counter()
                algorithm.preparation(rectangles)
                end = perf_counter()
                tmp_prep.append(end - start)
                start = perf_counter()
                for x, y in queries:
                    algorithm.query(x, y)
                end = perf_counter()
                tmp_quer.append(end - start)
            preparation_dict[label].append(sum(tmp_prep) / REPEAT)
            query_dict[label].append(sum(tmp_quer) / REPEAT)
            print(f"n=%s %s algorithm: Preparation: %s; Queries: %s;" % (
                (str(n)+";").ljust(5, " "), label.rjust(23, " "),
                result_format(preparation_dict[label][-1]),
                result_format(query_dict[label][-1])
            ), sep="")
    draw_graph(preparation_dict, values, "Preparation time (log)", True)
    draw_graph(query_dict, values, "Query time (log)", True)
    draw_graph(preparation_dict, values, "Preparation time ", False)
    draw_graph(query_dict, values, "Query time", False)


test(12)
