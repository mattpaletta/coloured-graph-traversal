from unittest import TestCase
from colouring.traversal import traverse_graph, Node, Colour


class TestTraversal(TestCase):
    def test_empty_graph(self):
        result = traverse_graph(graph = {},
                                node_colour = {},
                                target_colours = [])
        assert list(result) == [], "Empty graph returns empty list."
