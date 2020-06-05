import logging
from copy import deepcopy
from typing import List, Dict, Iterator, Set
import itertools

from colouring.colour import Colour
from colouring.matrix import Matrix
from colouring.node import Node
from colouring import utils

def combine_adj_matrix(starting_node: int, graph1: Matrix, graph2: Matrix) -> Matrix:
    if graph1.equals(graph2):
        return graph1
    elif graph1.subset(graph2):
        return graph1
    elif graph2.subset(graph1):
        return graph2

    out = Matrix(graph1.size())

    def traverse(curr_node, visited: Set[int]):
        # Do nothing if we already visited the node
        if curr_node not in visited:
            # Get all outgoing edges
            all_outgoing = set(graph1.get_connected_lst(curr_node) + graph2.get_connected_lst(curr_node))
            visited.add(curr_node)
            for outgoing in all_outgoing:
                if outgoing not in visited:
                    out.add_edge(curr_node, outgoing)
                    traverse(outgoing, visited)
    traverse(starting_node, set())
    return out


# This gets all the paths from one starting node to one or more end nodes
def find_children(graph: Matrix,
                  starting_node: int,
                  has_visited: List[int],
                  remaining_targets: List[int],
                  curr_matrix: Matrix) -> Iterator[Matrix]:
    # Get all children of root.
    children_of_root = graph.get_connected_lst(starting_node)

    for child in children_of_root:
        if child == starting_node:
            logging.debug("Skipping duplicate node: {0}".format(child))
            continue

        if child in has_visited:
            logging.debug("Skipping visited child: {0}".format(child))
            continue

        if child in remaining_targets:  # We found one of our target nodes!
            logging.debug("Found a child node: {0}".format(child))
            # TODO: Bug here is two found nodes have the same parent, (not in serial), this algorithm fails.

            # Remove child from target nodes, and recurse
            remaining_children = [x for x in remaining_targets if x != child]
        else:
            # We didn't hit a child, so no changes.
            remaining_children = remaining_targets

        # Add an edge between the current node and the child
        new_matrix = deepcopy(curr_matrix)
        new_matrix.add_edge(starting_node, child)

        if len(remaining_children) == 0:
            # We've found all children, we're done!
            yield new_matrix
        else:
            yield from find_children(graph = graph,
                                     starting_node = child,
                                     # Make sure we don't go in circles
                                     has_visited = has_visited + [child],
                                     remaining_targets = remaining_children,
                                     curr_matrix = new_matrix)

def traverse_graph(graph: Dict[Node, List[Node]], target_colours: List[Colour]) \
        -> Iterator[Dict[Node, List[Node]]]:
    nodes = list(graph.keys())
    num_nodes = len(nodes)
    graph_matrix = utils.adj_to_matrix(graph)

    # Lookup all nodes with that same colour
    node_colour_lookup: Dict[Colour, List[Node]] = build_node_colour_lookup(list(graph.keys()))

    starting_nodes: Iterator[List[int]] = get_all_starting_nodes(
        nodes = nodes,
        targets = target_colours,
        node_colours = node_colour_lookup)
    green_nodes: List[int] = utils.node_to_index(nodes, node_colour_lookup.get(Colour.GREEN, []))
    all_final_mat_output: List[Matrix] = []
    # We must start at the green nodes, so if they aren't present, we know there's no solution
    # Try it from every green node
    for green in green_nodes:
        # Get every set of end-nodes, try and build a graph to each set
        for target_nodes_set in starting_nodes:
            # store adjacency matrix from the particular green node to the particular target node
            green_to_target: List[Matrix] = []
            # Go to each individual target node
            for target_node in target_nodes_set:
                green_to_target.extend(list(find_children(
                    graph = graph_matrix,
                    starting_node = green,
                    has_visited = [green],  # Make sure we don't go in circles
                    remaining_targets = [target_node],
                    curr_matrix = Matrix(size = num_nodes))))
            if len(target_nodes_set) == 1:
                # There's only one node we're looking for, so output all paths to that node
                for completed_matrix in green_to_target:
                    completed_adj = utils.matrix_to_adj(nodes, completed_matrix)
                    yield completed_adj
            else:
                # Once we've gotten paths between that green node and every target node in the set, it's time to combine them and check!
                for combination in itertools.combinations(range(len(green_to_target)), r = len(target_nodes_set)):
                    # Create the merged graph
                    merged = Matrix(size = num_nodes)
                    for c in combination:
                        merged = combine_adj_matrix(green, green_to_target[c], merged)

                    # G1 and G2 are the two adjacency lists to combine from green_to_target
                    # They will have the same starting node, but different ending node
                    # Determine if we've already output it
                    if not utils.has_prev_output_graph(all_final_mat_output, merged):
                        # Determine if it meets all criteria
                        # (does it contain all of the target nodes)
                        did_get_all_targets = True
                        for target in target_nodes_set:
                            did_get_all_targets = did_get_all_targets and len(merged.inward_edges_lst(target)) > 0

                        # Determine if we got them all
                        if did_get_all_targets:
                            all_final_mat_output.append(merged)
                            merged_adj = utils.matrix_to_adj(nodes, merged)
                            yield merged_adj

def build_node_colour_lookup(nodes: List[Node]) -> Dict[Colour, List[Node]]:
    # Given a graph, return a dictionary containing a key as a colour, and a list of nodes that are that colour.
    output: Dict[Colour, List[Node]] = {}

    for node in nodes:
        node_colour: Colour = node.get_colour()
        # Append it to the other nodes we have with that colour, get the empty list if this is the first one.
        output.update({node_colour: [node] + output.get(node_colour, [])})

    return output

def get_all_starting_nodes(nodes: List[Node], targets: List[Colour], node_colours: Dict[Colour, List[Node]]) -> Iterator[List[int]]:
    # Get all possible combination of Nodes that are Colour
    # given -> [[A], [B], [C, D]]
    # output1 -> [A, B, C]
    # output2 -> [A, B, D]

    # Output one of each 'type' from targets
    def join(sub_plan_data: List[Colour]) -> Iterator[List[Node]]:
        if len(sub_plan_data) == 0:
            yield []
        else:
            current_colour = sub_plan_data.pop()
            # Join this one with the yielded result from the previous
            for sub_plans in join(sub_plan_data):
                for current_data_node in node_colours.get(current_colour, []):
                    yield sub_plans + [current_data_node]

    for result in join(sub_plan_data = targets):
        # Return just the indices of the nodes in the plan
        node_indices = utils.node_to_index(nodes, result)
        yield node_indices
