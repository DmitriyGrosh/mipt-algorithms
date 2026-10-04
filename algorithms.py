from collections import deque


def bfs(graph, start):
    visited = {start}
    queue = deque([start])
    order = []
    while queue:
        vertex = queue.popleft()
        order.append(vertex)
        for neighbor in sorted(graph[vertex]):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return order


def bfs_distances(graph, start):
    distances = {start: 0}
    queue = deque([start])
    while queue:
        vertex = queue.popleft()
        for neighbor in sorted(graph[vertex]):
            if neighbor not in distances:
                distances[neighbor] = distances[vertex] + 1
                queue.append(neighbor)
    return distances


def dfs(graph, start, visited=None, order=None):
    if visited is None:
        visited, order = set(), []
    visited.add(start)
    order.append(start)
    for neighbor in sorted(graph[start]):
        if neighbor not in visited:
            dfs(graph, neighbor, visited, order)
    return order


def topological_sort(nodes, graph, rev_graph):
    in_degree = {vertex: 0 for vertex in nodes}
    for vertex in nodes:
        in_degree[vertex] = len(graph[vertex])

    queue = deque(v for v in nodes if in_degree[v] == 0)
    batches = []
    done = 0

    while queue:
        batch = []
        for _ in range(len(queue)):
            vertex = queue.popleft()
            batch.append(vertex)
        batch.sort()
        batches.append(batch)
        done += len(batch)

        for vertex in batch:
            for dependent in rev_graph[vertex]:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)

    if done != len(nodes):
        return None, done
    return batches, done


def find_cycles(nodes, graph):
    white, gray, black = 0, 1, 2
    color = {vertex: white for vertex in nodes}
    cycles = []
    path = []
    pos_on_path = {}

    def dfs_visit(vertex):
        color[vertex] = gray
        path.append(vertex)
        pos_on_path[vertex] = len(path) - 1
        for neighbor in sorted(graph[vertex]):
            if color[neighbor] == gray:
                i = pos_on_path[neighbor]
                cycles.append(path[i:] + [neighbor])
            elif color[neighbor] == white:
                dfs_visit(neighbor)
        path.pop()
        del pos_on_path[vertex]
        color[vertex] = black

    for start in sorted(nodes):
        if color[start] == white:
            dfs_visit(start)
    return cycles


def run_stats(nodes, graph, rev_graph):
    n = len(nodes)
    m = sum(len(adj) for adj in graph.values())
    avg_deg = m / n if n > 0 else 0.0

    no_deps = sum(1 for v in nodes if len(graph[v]) == 0)
    orphans = sum(1 for v in nodes if len(rev_graph[v]) == 0)

    undirected = {vertex: set() for vertex in nodes}
    for vertex in nodes:
        undirected[vertex] |= graph[vertex]
        undirected[vertex] |= rev_graph[vertex]
    seen = set()
    components = 0
    for start in nodes:
        if start in seen:
            continue
        components += 1
        for vertex in bfs(undirected, start):
            seen.add(vertex)

    print("Число вершин:", n)
    print("Число ребер:", m)
    print("Средняя степень вершины:", round(avg_deg, 2))
    print("Число файлов без зависимостей:", no_deps)
    print("Число файлов, от которых не зависит никто:", orphans)
    print("Число слабосвязных компонент:", components)


def run_impact(nodes, rev_graph, target_file):
    if target_file in nodes:
        target = target_file
    else:
        matches = [v for v in nodes if v.endswith(target_file)]
        if len(matches) == 1:
            target = matches[0]
        else:
            print("Файл", target_file, "не найден.")
            return

    distances = bfs_distances(rev_graph, target)
    layers = {}
    for vertex, layer in distances.items():
        if layer == 0:
            continue
        layers.setdefault(layer, []).append(vertex)

    affected = len(distances) - 1
    print("Изменение", target, "затронет файлов:", affected)

    for layer in sorted(layers):
        if layer == 1:
            desc = "напрямую"
        elif layer == 2:
            desc = "через одного посредника"
        else:
            desc = "через " + str(layer - 1) + " посредников"

        files = layers[layer]
        print()
        print("Слой", layer, "(" + desc + ",", len(files), "файлов):")
        for file_name in files:
            print("  -", file_name)


def run_order(nodes, graph, rev_graph):
    batches, done = topological_sort(nodes, graph, rev_graph)
    if batches is None:
        progress = str(done) + "/" + str(len(nodes))
        print("Граф содержит циклы. Сортировка остановилась на", progress, "вершинах.")
        return

    batch_num = 1
    for batch in batches:
        print("Пачка", batch_num, "(" + str(len(batch)) + " файлов):")
        for file_name in batch:
            print(" ", file_name)
        batch_num += 1

    nb = len(batches)
    ratio = nb / len(nodes) if len(nodes) > 0 else 0.0
    print()
    print("Число пачек:", nb)
    print("Отношение к числу файлов:", round(ratio, 4))
