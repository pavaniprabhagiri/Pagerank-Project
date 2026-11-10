"""Reading graphs from files."""
import re
from typing import List, Tuple


def load_edges(path: str) -> List[Tuple[str, str]]:
    """Read an edge list. Each line: `source target` (space, tab or comma separated).

    Blank lines and lines starting with '#' are ignored.
    """
    edges = []
    with open(path, encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p for p in re.split(r"[,\s]+", line) if p]
            if len(parts) != 2:
                raise ValueError(f"{path}:{lineno}: expected 'source target', got {line!r}")
            edges.append((parts[0], parts[1]))
    return edges
