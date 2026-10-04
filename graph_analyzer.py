import os
import sys

from algorithms import find_cycles, run_impact, run_order, run_stats
from parser import build_graph


def main():
    if len(sys.argv) < 3:
        print("Использование: python3 graph_analyzer.py <stats|impact|cycles|order> <путь> [файл]")
        sys.exit(1)

    cmd = sys.argv[1]
    repo_path = sys.argv[2]
    nodes, graph, rev_graph = build_graph(repo_path)

    if cmd == "stats":
        run_stats(nodes, graph, rev_graph)
    elif cmd == "impact":
        if len(sys.argv) < 4:
            print("Укажите файл для анализа")
            sys.exit(1)
        root = os.path.abspath(repo_path)
        arg = sys.argv[3]
        if os.path.isabs(arg):
            path = arg
        else:
            path = os.path.join(root, arg)
        run_impact(nodes, rev_graph, os.path.relpath(path, root))
    elif cmd == "cycles":
        cycles = find_cycles(nodes, graph)
        if not cycles:
            print("Циклов не обнаружено")
            sys.exit(0)
        print("Найдено циклов:", len(cycles))
        for index, cycle in enumerate(cycles, 1):
            print("Цикл #" + str(index) + ":", " -> ".join(cycle))
        sys.exit(1)
    elif cmd == "order":
        run_order(nodes, graph, rev_graph)
    else:
        print("Неизвестная команда:", cmd)
        sys.exit(1)


if __name__ == "__main__":
    main()
