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

# This method does the reverse of index_to_nodes
# Takes a graph of nodes, and reverts back to indexes for easier printing/debugging
def nodes_to_index(nodes: List[Node], graph: Dict[Node, List[Node]]) -> Dict[int, List[int]]:
    out: Dict[int, List[int]] = {}
    def get_node_index(node: Node):
        for i in range(len(nodes)):
            if node.id == nodes[i].id:
                return i

    for k, v in graph.items():
        out[get_node_index(k)] = [get_node_index(i) for i in v]
    return out

class TestBlogExamples(TestCase):
    def test_example1(self):
        nodes = [Node(colour = Colour.GREEN, id = 1),
                 Node(colour = Colour.BLACK, id = 2),
                 Node(colour = Colour.RED, id = 3)]
        simple_graph = {
            0: [1, 2],
            1: [],
            2: []
        }
        node_graph = index_to_nodes(nodes, simple_graph)
        result = list(traverse_graph(graph = node_graph, target_colours = [Colour.RED]))
        assert len(result) == 1
    
    def test_example2(self):
        nodes = [Node(colour = Colour.GREEN, id = 1),
                 Node(colour = Colour.BLACK, id = 2),
                 Node(colour = Colour.RED, id = 3)]
        simple_graph = {
            0: [],
            1: [0],
            2: [0]
        }
        node_graph = index_to_nodes(nodes, simple_graph)
        result = list(traverse_graph(graph = node_graph, target_colours = [Colour.RED]))
        assert len(result) == 0
    
    def test_example3(self):
        nodes = [Node(colour = Colour.GREEN, id = 1),
                 Node(colour = Colour.BLACK, id = 2),
                 Node(colour = Colour.BLACK, id = 3),
                 Node(colour = Colour.BLACK, id = 4),
                 Node(colour = Colour.BLUE, id = 5),
                 Node(colour = Colour.BLACK, id = 6),
                 Node(colour = Colour.RED, id = 7)]
        simple_graph = {
            0: [1, 6],
            1: [2, 3],
            2: [],
            3: [],
            4: [0, 3],
            5: [4],
            6: [5],
        }
        node_graph = index_to_nodes(nodes, simple_graph)
        result = list(traverse_graph(graph = node_graph, target_colours = [Colour.RED, Colour.BLUE]))
        assert len(result) == 1
    
    def test_example4(self):
        nodes = [Node(colour = Colour.GREEN, id = 1),
                 Node(colour = Colour.BLACK, id = 2),
                 Node(colour = Colour.GREEN, id = 3),
                 Node(colour = Colour.BLACK, id = 4),
                 Node(colour = Colour.BLACK, id = 6),
                 Node(colour = Colour.BLUE, id = 7),
                 Node(colour = Colour.RED, id = 8)]
        simple_graph = {
            0: [1, 6],
            1: [2],
            2: [3, 4],
            3: [0, 5],
            4: [5, 6],
            5: [],
            6: [],
        }
        node_graph = index_to_nodes(nodes, simple_graph)
        result = list(traverse_graph(graph = node_graph, target_colours = [Colour.RED, Colour.BLUE]))
        #for graph in result:
        #    print("Printing solution")
        #    print(nodes_to_index(nodes, graph))
        assert len(result) == 4

