from typing import List, Dict

from colouring.matrix import Matrix
from colouring.node import Node

def has_prev_output_graph(list_of_output: List[Matrix], graph: Matrix) -> bool:
    for mat in list_of_output:
        if mat.equals(graph):
            return True
    return False

def matrix_to_adj_debug(graph: Matrix):
    out: Dict[int, List[int]] = {}
    for i in range(graph.size()):
        for j in range(graph.size()):
            if graph.get_edge(i, j):
                out[i] = out.get(i, []) + [j]
            else:
                out[i] = out.get(i, [])
    return out

def matrix_to_adj(nodes: List[Node], graph: Matrix):
    out: Dict[Node, List[Node]] = {}
    for i in range(graph.size()):
        for j in range(graph.size()):
            if graph.get_edge(i, j):
                out[nodes[i]] = out.get(nodes[i], []) + [nodes[j]]
            else:
                out[nodes[i]] = out.get(nodes[i], [])
    return out

def adj_to_matrix(graph: Dict[Node, List[Node]]) -> Matrix:
    all_nodes = list(graph.keys())
    m = Matrix(size = len(all_nodes))
    for k, v in graph.items():
        for connected_node in v:
            m.add_edge(all_nodes.index(k), all_nodes.index(connected_node))
    return m

def node_to_index(nodes: List[Node], lst: List[Node]) -> List[int]:
    return [nodes.index(n) for n in lst]
