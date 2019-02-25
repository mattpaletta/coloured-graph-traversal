from unittest import TestCase
from colouring.traversal import traverse_graph, Node, Colour, get_all_starting_nodes, build_node_lookup


class TestTraversal(TestCase):
    def test_empty_graph(self):
        result = traverse_graph(graph = {},
                                target_colours = [])
        assert list(result) == [], "Empty graph returns empty list."

    def test_single_graph(self):
        simple_graph = {
            Node(colour = Colour.GREEN, id = 1): [Node(colour = Colour.BLACK, id = 2)],
            Node(colour = Colour.BLACK, id = 2): [Node(colour = Colour.BLUE, id = 3)],
            Node(colour = Colour.BLUE, id = 3): []
        }
        result = traverse_graph(graph = simple_graph,
                                target_colours = [Colour.BLUE])
        print(list(result))

    def small_node_list(self):
        return [Node(colour = Colour.BLUE, id = 1),

                # Make sure we only have 1 red node.
                Node(colour = Colour.RED, id = 2),
                Node(colour = Colour.YELLOW, id = 3),
                Node(colour = Colour.BLUE, id = 4)]
