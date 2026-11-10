import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pagerank import build_graph, load_edges, pagerank


class PageRankTests(unittest.TestCase):
    def test_empty_graph(self):
        self.assertEqual(pagerank({}), ({}, 0))

    def test_scores_sum_to_one(self):
        g = build_graph([("A", "B"), ("B", "C"), ("C", "A"), ("D", "A")])
        ranks, _ = pagerank(g)
        self.assertAlmostEqual(sum(ranks.values()), 1.0, places=6)

    def test_symmetric_cycle_is_uniform(self):
        g = build_graph([("A", "B"), ("B", "C"), ("C", "A")])
        ranks, _ = pagerank(g)
        for v in ranks.values():
            self.assertAlmostEqual(v, 1 / 3, places=6)

    def test_most_linked_page_ranks_highest(self):
        g = build_graph([("A", "C"), ("B", "C"), ("D", "C"), ("C", "A")])
        ranks, _ = pagerank(g)
        self.assertEqual(max(ranks, key=ranks.get), "C")

    def test_dangling_nodes_keep_sum_one(self):
        g = build_graph([("A", "B"), ("A", "C")])  # B and C are dangling
        ranks, _ = pagerank(g)
        self.assertAlmostEqual(sum(ranks.values()), 1.0, places=6)

    def test_invalid_damping(self):
        with self.assertRaises(ValueError):
            pagerank({"A": set()}, damping=1.5)

    def test_load_edges(self):
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
            f.write("# comment\nA B\nB,C\n\n")
            path = f.name
        try:
            self.assertEqual(load_edges(path), [("A", "B"), ("B", "C")])
        finally:
            os.remove(path)

    def test_load_edges_bad_line(self):
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
            f.write("A B C\n")
            path = f.name
        try:
            with self.assertRaises(ValueError):
                load_edges(path)
        finally:
            os.remove(path)


if __name__ == "__main__":
    unittest.main()
