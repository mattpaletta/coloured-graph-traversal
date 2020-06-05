from unittest import TestCase
from colouring.matrix import Matrix
from colouring import utils
from colouring.traversal import Node, Colour, get_all_target_nodes, build_node_colour_lookup


class TestUtils(TestCase):
    def test_build_node_lookup(self):
        graph_nodes = self.small_node_list()
        node_colours = build_node_colour_lookup(nodes = graph_nodes)

    def test_starting_nodes_single_target_single(self):
        graph_nodes = self.small_node_list()
        result = get_all_target_nodes(
                nodes = graph_nodes,
                targets = [Colour.RED],
                node_colours = build_node_colour_lookup(nodes = graph_nodes))
        node_ids = []
        for sequence in result:
            node_ids.append(sequence)
        assert node_ids == [[1]], "Starting nodes not adding the correct nodes to sequence"

    def test_starting_nodes_single_target_multiple(self):
        graph_nodes = self.small_node_list()
        result = get_all_target_nodes(
                nodes = graph_nodes,
                targets = [Colour.BLUE],
                node_colours = build_node_colour_lookup(nodes = graph_nodes))
        node_ids = []
        for sequence in result:
            node_ids.append(sequence)
        assert node_ids == [[3], [0]], "Starting (multiple) nodes not adding the correct nodes to sequence."

    def test_starting_nodes_multiple_target_single(self):
        graph_nodes = self.small_node_list()
        result = get_all_target_nodes(
                nodes = graph_nodes,
                targets = [Colour.YELLOW, Colour.RED],
                node_colours = build_node_colour_lookup(nodes = graph_nodes))
        node_ids = []
        for sequence in result:
            node_ids.append(sequence)
        assert node_ids == [[2, 1]], "Starting (multiple) nodes not adding the correct nodes to sequence."

    def test_has_prev_output(self):
        a = Matrix(size = 3)
        b = Matrix(size = 3)
        c = Matrix(size = 3)

        a.add_edge(0, 1)
        b.add_edge(1, 2)
        c.add_edge(0, 2)

        prev_output = [a, b]
        assert not utils.has_prev_output_graph(prev_output, c)
        assert utils.has_prev_output_graph(prev_output, a)

    def test_matrix_to_adj(self):
        a = Matrix(size = 2)
        a.add_edge(0, 1)
        nodes = [Node(colour = Colour.BLUE, id = 1),
                 Node(colour = Colour.BLACK, id = 2)]
        result = utils.matrix_to_adj(nodes, a)
        assert result.get(nodes[0], []) == [nodes[1]]

    def test_matrix_to_adj_debug(self):
        a = Matrix(size = 2)
        a.add_edge(0, 1)
        result = utils.matrix_to_adj_debug(a)
        assert result.get(0, []) == [1]

    def small_node_list(self):
        return [Node(colour = Colour.BLUE, id = 1),

                # Make sure we only have 1 red node.
                Node(colour = Colour.RED, id = 2),
                Node(colour = Colour.YELLOW, id = 3),
                Node(colour = Colour.BLUE, id = 4)]
