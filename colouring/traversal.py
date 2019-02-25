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
    def __init__(self, colour: Colour):
        self._colour = colour

    def is_colour(self, colour: Colour) -> bool:
        return self._colour.value == colour.value


def traverse_graph(graph: Dict[Node, List[Node]], node_colour: Dict[Node, Colour], target_colours: List[Colour]) \
        -> Iterator[Dict[Node, List[Node]]]:

    # Lookup all nodes with that same colour
    node_colour_lookup: Dict[Colour, List[Node]] = {}

    def find_children(starting_node: Node,
                      has_visited: List[Node],
                      remaining_targets: List[Node],
                      curr_adj: Dict[Node, List[Node]]) -> Iterator[Dict[Node, List[Node]]]:

        # Get all children of root.
        children_of_root = graph.get(starting_node, [])
        for child in children_of_root:
            child_name = child.__name__
            if child_name in has_visited:
                logging.debug("Skipping visited child: " + child_name)
                continue
            if child_name == starting_node.__class__.__name__:
                logging.debug("Skipping duplicate node:" + child_name)
                continue

            if child in remaining_targets:  # We found one of our target nodes!
                logging.debug("Found a child node: " + child_name)

                # Remove child from target nodes, and recurse
                remaining_children = [x for x in remaining_targets if x != child]
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

    starting_nodes = __get_all_starting_nodes(target_colours, node_colour_lookup)

    green_nodes = node_colour_lookup.get(Colour.GREEN, [])
    if len(green_nodes) > 1:
        for green in green_nodes:
            for target_nodes in starting_nodes:
                yield from find_children(starting_node = green,
                                 has_visited = [green],  # Make sure we don't go in circles
                                 remaining_targets = target_nodes,
                                 curr_adj = {})


def __get_all_starting_nodes(targets: List[Colour], all_node_colours: Dict[Colour, List[Node]]) -> Iterator[List[Node]]:
    # Get all possible combination of Nodes that are Colour
    # given -> [[A], [B], [C, D]]
    # output1 -> [A, B, C]
    # output2 -> [A, B, D]

    # Output one of each 'type' from targets
    def join(sub_plan_data: List[Colour]) -> Iterator[List[Node]]:
        if len(sub_plan_data) == 0:
            yield []
        elif len(sub_plan_data) == 1:
            yield list(self._goal_input_adj.get(sub_plan_data[0].name))
        else:
            current_plan_data: targets = sub_plan_data.pop()
            # Join this one with the yielded result from the previous
            for sub_plans in join(sub_plan_data):
                for current_data_node in self._goal_input_adj.get(self.__value_class_to_str(current_plan_data.name), []):
                    yield sub_plans + [current_data_node]

    yield from join(sub_plan_data = targets)
