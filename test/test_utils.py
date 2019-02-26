from unittest import TestCase
from colouring.traversal import Node, Colour, get_all_starting_nodes, build_node_lookup


class TestUtils(TestCase):
    def test_build_node_lookup(self):
        graph_nodes = self.small_node_list()
        node_colours = build_node_lookup(nodes = graph_nodes)

        # Make sure the right nodes are placed in the right place.
        assert sorted(map(lambda n: n.id, node_colours.get(Colour.RED))) == [2]
        assert sorted(map(lambda n: n.id, node_colours.get(Colour.BLUE))) == [1, 4]
        assert sorted(map(lambda n: n.id, node_colours.get(Colour.YELLOW))) == [3]

    def test_starting_nodes_single_target_single(self):
        graph_nodes = self.small_node_list()
        result = get_all_starting_nodes(targets = [Colour.RED],
                                        node_colours = build_node_lookup(nodes = graph_nodes))
        node_ids = []
        for sequence in result:
            node_ids.append(list(map(lambda n: n.id, sequence)))
        assert node_ids == [[2]], "Starting nodes not adding the correct nodes to sequence"

    def test_starting_nodes_single_target_multiple(self):
        graph_nodes = self.small_node_list()
        result = get_all_starting_nodes(targets = [Colour.BLUE],
                                        node_colours = build_node_lookup(nodes = graph_nodes))
        node_ids = []
        for sequence in result:
            node_ids.append(list(map(lambda n: n.id, sequence)))
        assert node_ids == [[4], [1]], "Starting (multiple) nodes not adding the correct nodes to sequence."

    def test_starting_nodes_multiple_target_single(self):
        graph_nodes = self.small_node_list()
        result = get_all_starting_nodes(targets = [Colour.YELLOW, Colour.RED],
                                        node_colours = build_node_lookup(nodes = graph_nodes))
        node_ids = []
        for sequence in result:
            node_ids.append(list(map(lambda n: n.id, sequence)))
        assert node_ids == [[3, 2]], "Starting (multiple) nodes not adding the correct nodes to sequence."

    def small_node_list(self):
        return [Node(colour = Colour.BLUE, id = 1),
                
                # Make sure we only have 1 red node.
                Node(colour = Colour.RED, id = 2),
                Node(colour = Colour.YELLOW, id = 3),
                Node(colour = Colour.BLUE, id = 4)]
