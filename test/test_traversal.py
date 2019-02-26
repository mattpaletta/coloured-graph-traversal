from unittest import TestCase
from colouring.traversal import traverse_graph, Node, Colour, get_all_starting_nodes, build_node_lookup


class TestTraversal(TestCase):
    def test_empty_graph(self):
        result = traverse_graph(graph = {},
                                target_colours = [])
        assert list(result) == [], "Empty graph returns empty list."

    def test_single_graph(self):
        nodes = [Node(colour = Colour.GREEN, id = 1),
                 Node(colour = Colour.BLACK, id = 2),
                 Node(colour = Colour.BLUE, id = 3)]
        simple_graph = {
            nodes[0]: [nodes[1]],
            nodes[1]: [nodes[2]],
            nodes[2]: []
        }
        result = traverse_graph(graph = simple_graph,
                                target_colours = [Colour.BLUE])
        for key in result:
            for k, v in key.items():
                node_entry = simple_graph.get(list(filter(lambda x: x.id == k.id, nodes))[0])

                # Check to make sure the ID's of every child node are the same.
                assert list(map(lambda n: n.id, node_entry)) == list(map(lambda n: n.id, v))

    def test_multiple_invalid_graph(self):
        nodes = [Node(colour = Colour.GREEN, id = 1),
                 Node(colour = Colour.BLACK, id = 2),
                 Node(colour = Colour.BLUE, id = 3)]
        simple_graph = {
            nodes[0]: [nodes[1]],
            nodes[1]: [nodes[2]],
            nodes[2]: []
        }
        result = traverse_graph(graph = simple_graph,
                                target_colours = [Colour.BLUE, Colour.RED])
        final = list(result)
        assert len(list(result)) == 0, "Should not return any valid graphs."

    def test_multiple_valid_graph_serial_parents(self):
        nodes = [Node(colour = Colour.GREEN, id = 1),
                 Node(colour = Colour.BLACK, id = 2),
                 Node(colour = Colour.BLACK, id = 3),
                 Node(colour = Colour.BLUE, id = 4),
                 Node(colour = Colour.RED, id = 5)]
        simple_graph = {
            nodes[0]: [nodes[1]],
            nodes[1]: [nodes[2]],
            nodes[2]: [nodes[3]],
            nodes[3]: [nodes[4]],
            nodes[4]: [],
        }
        result = traverse_graph(graph = simple_graph,
                                target_colours = [Colour.BLUE, Colour.RED])
        final = list(result)
        assert len(final[0]) == 5, "Should contain one of every node."

    def small_node_list(self):
        return [Node(colour = Colour.BLUE, id = 1),

                # Make sure we only have 1 red node.
                Node(colour = Colour.RED, id = 2),
                Node(colour = Colour.YELLOW, id = 3),
                Node(colour = Colour.BLUE, id = 4)]
