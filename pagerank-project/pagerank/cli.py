"""Command-line interface."""
import argparse
import csv
import sys

from .core import build_graph, pagerank
from .io import load_edges


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="pagerank", description="Compute PageRank for a link graph.")
    p.add_argument("edges", help="edge-list file (one 'source target' per line)")
    p.add_argument("-d", "--damping", type=float, default=0.85, help="damping factor (default 0.85)")
    p.add_argument("-t", "--tol", type=float, default=1e-6, help="convergence tolerance (default 1e-6)")
    p.add_argument("-m", "--max-iter", type=int, default=100, help="max iterations (default 100)")
    p.add_argument("-n", "--top", type=int, default=10, help="show top N pages (default 10)")
    p.add_argument("-o", "--output", help="also save full results to this CSV file")
    args = p.parse_args(argv)

    try:
        graph = build_graph(load_edges(args.edges))
        ranks, iters = pagerank(graph, args.damping, args.tol, args.max_iter)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    ordered = sorted(ranks.items(), key=lambda kv: (-kv[1], kv[0]))
    print(f"Nodes: {len(graph)}  Iterations: {iters}  Damping: {args.damping}\n")
    print(f"{'Rank':<5} {'Page':<20} {'Score':>10}")
    print("-" * 37)
    for i, (node, score) in enumerate(ordered[: args.top], 1):
        print(f"{i:<5} {node:<20} {score:>10.6f}")

    if args.output:
        with open(args.output, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["rank", "page", "score"])
            for i, (node, score) in enumerate(ordered, 1):
                w.writerow([i, node, f"{score:.8f}"])
        print(f"\nFull results saved to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
