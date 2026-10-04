import sys
import networkx as nx
from parser import build_graph

if len(sys.argv) < 2:
    print("Использование: python verify.py <путь>")
    sys.exit(1)

nodes, graph, _ = build_graph(sys.argv[1])

g = nx.DiGraph()
g.add_nodes_from(nodes)
for u, deps in graph.items():
    for v in deps:
        g.add_edge(u, v)

cycles = list(nx.simple_cycles(g))
print("Циклы:", len(cycles))

if nx.is_directed_acyclic_graph(g):
    print("Длина топологического порядка:", len(list(nx.topological_sort(g))))
else:
    print("Топологический порядок: невозможно построить из-за циклов")