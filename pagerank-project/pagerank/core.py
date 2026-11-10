"""Core PageRank algorithm (power iteration)."""
from typing import Dict, Iterable, Set, Tuple

Graph = Dict[str, Set[str]]


def build_graph(edges: Iterable[Tuple[str, str]]) -> Graph:
    """Build an adjacency map {node: set(outgoing neighbours)} from (src, dst) edges.

    Every node that appears anywhere (even only as a target) is included.
    Duplicate edges are ignored.
    """
    graph: Graph = {}
    for src, dst in edges:
        graph.setdefault(src, set()).add(dst)
        graph.setdefault(dst, set())
    return graph


def pagerank(
    graph: Graph,
    damping: float = 0.85,
    tol: float = 1e-6,
    max_iter: int = 100,
) -> Tuple[Dict[str, float], int]:
    """Compute PageRank with power iteration.

    PR(v) = (1-d)/N + d * ( sum_{u->v} PR(u)/outdeg(u) + dangling/N )

    Dangling nodes (no outgoing links) spread their rank evenly over all nodes,
    so the scores always sum to 1.

    Returns (ranks, iterations_used).
    """
    if not 0 < damping < 1:
        raise ValueError("damping must be between 0 and 1 (exclusive)")
    if tol <= 0:
        raise ValueError("tol must be positive")
    if max_iter < 1:
        raise ValueError("max_iter must be at least 1")

    nodes = list(graph)
    n = len(nodes)
    if n == 0:
        return {}, 0

    incoming = {v: [] for v in nodes}
    for u, outs in graph.items():
        for v in outs:
            incoming[v].append(u)

    rank = {v: 1.0 / n for v in nodes}
    iterations = 0
    for iterations in range(1, max_iter + 1):
        dangling = sum(rank[u] for u in nodes if not graph[u])
        base = (1.0 - damping) / n + damping * dangling / n
        new_rank = {
            v: base + damping * sum(rank[u] / len(graph[u]) for u in incoming[v])
            for v in nodes
        }
        diff = sum(abs(new_rank[v] - rank[v]) for v in nodes)
        rank = new_rank
        if diff < tol:
            break
    return rank, iterations
