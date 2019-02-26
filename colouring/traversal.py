import logging
from copy import deepcopy
from enum import Enum
from typing import List, Dict, Iterator


class Colour(Enum):
    BLACK = 1
    RED = 2
    GREEN = 3
    BLUE = 4
    YELLOW = 5


class Node(object):
    def __init__(self, colour: Colour, id: int):
        self._colour = colour
        self.id = id

    def is_colour(self, colour: Colour) -> bool:
        return self.get_colour().value == colour.value

    def get_colour(self) -> Colour:
        return self._colour


def traverse_graph(graph: Dict[Node, List[Node]], target_colours: List[Colour]) \
        -> Iterator[Dict[Node, List[Node]]]:

    # Lookup all nodes with that same colour
    node_colour_lookup: Dict[Colour, List[Node]] = build_node_lookup(list(graph.keys()))

    def find_children(starting_node: Node,
                      has_visited: List[Node],
                      remaining_targets: List[Node],
                      curr_adj: Dict[Node, List[Node]]) -> Iterator[Dict[Node, List[Node]]]:

        # Get all children of root.
        children_of_root = graph.get(starting_node, [])
        for child in children_of_root:
            child_name = child.id
            if child_name in has_visited:
                logging.debug("Skipping visited child: {0}".format(child_name))
                continue
            if child_name == starting_node.id:
                logging.debug("Skipping duplicate node: {0}".format(child_name))
                continue

            if child in remaining_targets:  # We found one of our target nodes!
                logging.debug("Found a child node: {0}".format(child_name))
                # TODO: Bug here is two found nodes have the same parent, (not in serial), this algorithm fails.

                # Remove child from target nodes, and recurse
                remaining_children = [x for x in remaining_targets if x.id != child.id]
            else:
                # We didn't hit a child, so no changes.
                remaining_children = remaining_targets

            # Add the child to the adjacency list for recurse.
            new_adj = deepcopy(curr_adj)
            new_adj.update({starting_node: [child] + new_adj.get(starting_node, [])})

            if len(remaining_children) == 0:
                # We've found all children, we're done!
                new_adj.update({child: []})
                yield new_adj
            else:
                yield from find_children(starting_node = child,
                                         # Make sure we don't go in circles
                                         has_visited = has_visited + [child_name],
                                         remaining_targets = remaining_children,
                                         curr_adj = new_adj)

    starting_nodes = get_all_starting_nodes(targets = target_colours,
                                            node_colours = node_colour_lookup)
    green_nodes = node_colour_lookup.get(Colour.GREEN, [])

    if len(green_nodes) > 0:
        for target_nodes in starting_nodes:
            for green in green_nodes:
                yield from find_children(starting_node = green,
                                         has_visited = [green],  # Make sure we don't go in circles
                                         remaining_targets = target_nodes,
                                         curr_adj = {})


def build_node_lookup(nodes: List[Node]) -> Dict[Colour, List[Node]]:
    # Given a graph, return a dictionary containing a key as a colour, and a list of nodes that are that colour.

    output: Dict[Colour, List[Node]] = {}

    for node in nodes:
        node_colour: Colour = node.get_colour()

        # Append it to the other nodes we have with that colour, get the empty list if this is the first one.
        output.update({node_colour: [node] + output.get(node_colour, [])})

    return output


def get_all_starting_nodes(targets: List[Colour],
                           node_colours: Dict[Colour, List[Node]]) -> Iterator[List[Node]]:

    # Get all possible combination of Nodes that are Colour
    # given -> [[A], [B], [C, D]]
    # output1 -> [A, B, C]
    # output2 -> [A, B, D]

    # Output one of each 'type' from targets
    def join(sub_plan_data: List[Colour]) -> Iterator[List[Node]]:
        if len(sub_plan_data) == 0:
            yield []
        elif len(sub_plan_data) == 1 and len(targets) > 1:
            yield list(node_colours.get(sub_plan_data[0]))
        else:
            current_colour = sub_plan_data.pop()
            # Join this one with the yielded result from the previous
            for sub_plans in join(sub_plan_data):
                for current_data_node in node_colours.get(current_colour, []):
                    yield sub_plans + [current_data_node]

    yield from join(sub_plan_data = targets)
