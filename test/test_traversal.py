from unittest import TestCase
from colouring.traversal import traverse_graph, Node, Colour
from typing import List, Dict

# Helper function, takes a list of nodes, and a graph of their indices, returns the nodes at those indices
# Ex:
# nodes = [Node(1), Node(2), Node(3)]
# graph = {
#   0 : [1],
#   1 : [2],
#   2 : []
# }
# returns = {
#    Node(1) : [Node(2)],
#    Node(2) : [Node(3)],
#    Node(3) : []
# }
def index_to_nodes(nodes: List[Node], graph: Dict[int, List[int]]) -> Dict[Node, List[Node]]:
    out: Dict[Node, List[Node]] = {}
    for k, v in graph.items():
        out[nodes[k]] = [nodes[i] for i in v]
    return out

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

    def test_multiple_target_valid_graph_serial_parents(self):
        nodes = [Node(colour = Colour.GREEN, id = 1),
                 Node(colour = Colour.BLACK, id = 2),
                 Node(colour = Colour.BLACK, id = 3),
                 Node(colour = Colour.BLUE, id = 4),
                 Node(colour = Colour.RED, id = 5)]
        simple_graph = {
            0: [1],
            1: [2],
            2: [3],
            3: [4],
            4: [],
        }
        node_graph = index_to_nodes(nodes, simple_graph)
        result = traverse_graph(graph = node_graph,
                                target_colours = [Colour.BLUE, Colour.RED])
        final = list(result)
        assert len(final[0].items()) == 5, "Should contain one of every node."

    def test_starting_node_cycle(self):
        nodes = [Node(colour = Colour.GREEN, id = 1),
                 Node(colour = Colour.BLACK, id = 2),
                 Node(colour = Colour.BLACK, id = 3),
                 Node(colour = Colour.BLUE, id = 4)]
        simple_graph = {
            0 : [1],
            1 : [2],
            2 : [0, 3],
            3 : [],
        }
        node_graph = index_to_nodes(nodes, simple_graph)
        result = list(traverse_graph(graph = node_graph,
                                target_colours = [Colour.BLUE]))
        assert len(result) == 1, "Failed to find the single correct graph"
        assert len(result[0]) == 4, "The correct graph should have 4 nodes"


    def test_cycle_single_parent(self):
        nodes = [Node(colour = Colour.GREEN, id = 1),
                 Node(colour = Colour.BLACK, id = 2),
                 Node(colour = Colour.BLACK, id = 3),
                 Node(colour = Colour.BLACK, id = 4),
                 Node(colour = Colour.BLUE, id = 5)]
        simple_graph = {
            0 : [1],
            1 : [2, 3],
            2 : [3, 4],
            3 : [1, 4],
            4 : []
        }

        node_graph = index_to_nodes(nodes, simple_graph)
        result = list(traverse_graph(graph = node_graph, target_colours = [Colour.BLUE]))
        assert len(result) == 3, "Should have found all three target graphs"

    def test_cycle_multiple_parents(self):
        nodes = [Node(colour = Colour.GREEN, id = 1),
                 Node(colour = Colour.BLACK, id = 2),
                 Node(colour = Colour.BLACK, id = 3),
                 Node(colour = Colour.BLACK, id = 4),
                 Node(colour = Colour.BLUE, id = 5),
                 Node(colour = Colour.RED, id = 6)]
        simple_graph = {
            0 : [1],
            1 : [2, 3],
            2 : [3, 4],
            3 : [1, 4, 5],
            4 : [],
            5 : []
        }
        node_graph = index_to_nodes(nodes, simple_graph)
        result = list(traverse_graph(graph = node_graph, target_colours = [Colour.BLUE, Colour.RED]))
        # for graph in result:
        #    print("Printing solution")
        #    print(nodes_to_index(nodes, graph))
        assert len(result) == 4, "there are no graphs that satisfy this graph"

    def test_splitting_end_points(self):
        nodes = [Node(colour = Colour.GREEN, id = 1),
                 Node(colour = Colour.BLACK, id = 2),
                 Node(colour = Colour.BLACK, id = 3),
                 Node(colour = Colour.BLACK, id = 4),
                 Node(colour = Colour.BLUE, id = 5),
                 Node(colour = Colour.RED, id = 6),
                 Node(colour = Colour.BLACK, id = 7)]
        simple_graph = {
            0 : [1, 4, 5],
            1 : [2],
            2 : [3],
            3 : [3, 0, 4],
            4 : [],
            5 : [],
            6 : [4],
        }

        node_graph = index_to_nodes(nodes, simple_graph)
        result = list(traverse_graph(graph = node_graph, target_colours = [Colour.BLUE, Colour.RED]))
        assert len(result) == 2, "Should have found all three target graphs"
