"""A small, dependency-free PageRank implementation."""
from .core import build_graph, pagerank
from .io import load_edges

__all__ = ["build_graph", "pagerank", "load_edges"]
__version__ = "1.0.0"
