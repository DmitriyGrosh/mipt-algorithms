import ast
import os

SKIP_DIRS = {".venv", "venv", ".git", "node_modules", "__pycache__"}
TEST_DIRS = {"tests", "__tests__", "test"}


def parse_imports(filepath):
    found = []
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            tree = ast.parse(f.read(), filename=filepath)
    except Exception:
        return found

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                found.append((alias.name, 0))
        elif isinstance(node, ast.ImportFrom):
            module_name = node.module or ""
            found.append((module_name, node.level))
    return found


def path_for_module(root, parts):
    if not parts:
        return None
    rel_path = os.sep.join(parts)
    py_file = os.path.join(root, rel_path + ".py")
    if os.path.isfile(py_file):
        return os.path.relpath(py_file, root)
    init_file = os.path.join(root, rel_path, "__init__.py")
    if os.path.isfile(init_file):
        return os.path.relpath(init_file, root)
    return None


def resolve_import(root, current_file, module_name, level):
    rel_file = os.path.relpath(current_file, root)
    dir_parts = os.path.dirname(rel_file).split(os.sep)
    if dir_parts == [""]:
        dir_parts = []

    if level > 0:
        base = list(dir_parts)
        for _ in range(level - 1):
            if base:
                base.pop()
        if module_name:
            parts = base + module_name.split(".")
        else:
            parts = base
    else:
        parts = module_name.split(".")

    candidates = [parts]
    root_name = os.path.basename(root)
    if parts and parts[0] == root_name and len(parts) > 1:
        candidates.append(parts[1:])

    for candidate in candidates:
        resolved = path_for_module(root, candidate)
        if resolved is not None:
            return resolved
    return None


def iter_project_py_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]

        rel_dir = os.path.relpath(dirpath, root)
        if rel_dir != "." and any(p in TEST_DIRS for p in rel_dir.split(os.sep)):
            continue

        for filename in filenames:
            if filename.endswith(".py"):
                yield os.path.relpath(os.path.join(dirpath, filename), root)


def build_graph(root_path):
    root = os.path.abspath(root_path)
    nodes = set(iter_project_py_files(root))
    graph = {node: set() for node in nodes}
    rev_graph = {node: set() for node in nodes}

    for node in nodes:
        filepath = os.path.join(root, node)
        for module_name, level in parse_imports(filepath):
            dep = resolve_import(root, filepath, module_name, level)
            if dep is None or dep not in nodes or dep == node:
                continue
            graph[node].add(dep)
            rev_graph[dep].add(node)

    return nodes, graph, rev_graph
