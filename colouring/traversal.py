import logging
from copy import deepcopy
from enum import Enum
from typing import List, Dict, Iterator, Set
import itertools

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

def nodes_to_index(nodes, graph):
    out = {}
    def get_node_index(node):
        for i in range(len(nodes)):
            if node.id == nodes[i].id:
                return i
    for k, v in graph.items():
        out[get_node_index(k)] = [get_node_index(i) for i in v]
    return out

def is_adj_same(graph1: Dict[Node, List[Node]], graph2: Dict[Node, List[Node]]):
    # If their keys differ, they can't be the same
    if set(graph1.keys()) != set(graph2.keys()):
        return False
    else:
        for k in graph1.keys():
            # Make sure every key is the same
            if graph1.get(k) != graph2.get(k):
                return False
        return True

def combine_adj_list(starting_node: Node, graph1: Dict[Node, List[Node]], graph2: Dict[Node, List[Node]]) -> Dict[Node, List[Node]]:
    # Warning: There may be dangling nodes afterwards
    out = {}

    def node_by_id(node_id):
        result = [n for n in list(graph1.keys()) + list(graph2.keys()) if node_id == n.id]
        if len(result) > 0:
            return result[0]
        else:
            return None

    def traverse(curr_node, visited: Set[int]):
        curr_node_id = curr_node.id
        if curr_node_id in visited:
            # We've already visited this node, do nothing
            print("Already visited")
            pass
        else:
            # Get all outgoing edges
            all_outgoing = graph1.get(node_by_id(curr_node.id), []) + graph2.get(node_by_id(curr_node), [])
            visited.add(curr_node_id)
            print(all_outgoing)
            out[node_by_id(curr_node.id)] = all_outgoing
            for outgoing in all_outgoing:
                print("Traversing: ", curr_node_id, " to ", outgoing.id)
                traverse(outgoing, visited)
    traverse(node_by_id(starting_node.id), set())
    print(nodes_to_index(list(graph1.keys()) + list(graph2.keys()), out))
    return out
    """
    for k in graph1.keys():
        if k.id not in [n.id for n in out.keys()]:
            out[k] = list(set(graph1.get(k, []) + graph2.get(k, [])))

    for k in graph2.keys():
        # We can skip over items already in out (must have been in graph1)
        if k.id not in [n.id for n in out.keys()]:
            out[k] = list(set(graph1.get(k, []) + graph2.get(k, [])))
    """
    return out

def has_output_adj(list_of_output, graph):
    for adj in list_of_output:
        if is_adj_same(adj, graph):
            return True
    return False

def traverse_graph(graph: Dict[Node, List[Node]], target_colours: List[Colour]) \
        -> Iterator[Dict[Node, List[Node]]]:

    # Lookup all nodes with that same colour
    node_colour_lookup: Dict[Colour, List[Node]] = build_node_lookup(list(graph.keys()))



    # This gets all the paths from one starting node to one or more end nodes
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
    # End find_children function
    ####

    starting_nodes = get_all_starting_nodes(targets = target_colours,
                                            node_colours = node_colour_lookup)
    green_nodes = node_colour_lookup.get(Colour.GREEN, [])

    # We must start at the green nodes, so if they aren't present, we know there's no solution
    if len(green_nodes) > 0:
        all_final_adj_output = []
        # Try if from every green node
        for green in green_nodes:
            # Get every set of end-nodes, try and build a graph to each set
            for target_nodes_set in starting_nodes:
                # store adjacency lists from the particular green node to the particular target node
                green_to_target = []
                # Go to each individual target node
                for target_node in target_nodes_set:
                    green_to_target.extend(list(find_children(starting_node = green,
                                             has_visited = [green],  # Make sure we don't go in circles
                                             remaining_targets = [target_node],
                                             curr_adj = {})))
                if len(target_nodes_set) == 1:
                    yield from green_to_target
                else:
                    # Once we've gotten paths between that green node and every target node in the set, it's time to combine them and check!
                    for combination in itertools.combinations(range(len(green_to_target)), r = len(target_nodes_set)):
                        # Create the merged graph
                        merged = {}
                        for c in combination:
                            merged = combine_adj_list(green, green_to_target[c], merged)

                        # G1 and G2 are the two adjacency lists to combine from green_to_target
                        # They will have the same starting node, but different ending node
                        # Determine if we've already output it
                        if not has_output_adj(all_final_adj_output, merged):
                            # Determine if it meets all criteria
                            # (does it contain all of the target nodes)
                            target_node_ideal = []
                            for k in merged.keys():
                                # We only care about the target nodes
                                if k.id in [n.id for n in target_nodes_set]:
                                    target_node_ideal.append(k.id)
                            # Determine if we got them all
                            if set(target_node_ideal) == set(list(map(lambda n: n.id, target_nodes_set))):
                                all_final_adj_output.append(merged)
                                yield merged


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
