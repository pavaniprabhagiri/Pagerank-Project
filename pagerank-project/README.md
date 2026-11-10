# PageRank in Python

A clean, dependency-free implementation of Google's PageRank algorithm using power iteration.
Handles dangling nodes (pages with no outgoing links), duplicate edges and self-loops.

## Project structure

```
pagerank-project/
├── pagerank/
│   ├── __init__.py
│   ├── __main__.py      # enables `python -m pagerank`
│   ├── core.py          # the algorithm
│   ├── io.py            # edge-list loader
│   └── cli.py           # command-line interface
├── data/sample_edges.txt
├── tests/test_pagerank.py
├── requirements.txt
├── LICENSE
└── README.md
```

## How it works

For N pages and damping factor d (default 0.85):

```
PR(v) = (1 - d)/N + d * ( sum of PR(u)/outdegree(u) over every u linking to v  +  dangling_rank/N )
```

Start with every page at 1/N and repeat until the total change is below the tolerance.
Scores always sum to 1.

## Run

```bash
python -m pagerank data/sample_edges.txt
python -m pagerank data/sample_edges.txt --top 5 --damping 0.85 -o results.csv
```

Options: `-d/--damping`, `-t/--tol`, `-m/--max-iter`, `-n/--top`, `-o/--output`.

## Use as a library

```python
from pagerank import build_graph, pagerank

graph = build_graph([("A", "B"), ("B", "C"), ("C", "A")])
ranks, iterations = pagerank(graph)
print(ranks)
```

## Input format

One edge per line: `source target` (space, tab or comma separated). `#` starts a comment.

## Tests

```bash
python -m unittest discover -s tests -v
```

## License

MIT
