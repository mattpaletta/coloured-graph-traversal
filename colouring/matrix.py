from typing import List, Iterator
class Matrix(object):
    def __init__(self, size: int):
        self._data: List[List[bool]] = []
        for i in range(size):
            self._data.append([])
            for j in range(size):
                self._data[i].append(False)

        self._size = size

    def add_edge(self, from_node: int, to_node: int) -> None:
        assert from_node < self._size and to_node < self._size
        self._data[from_node][to_node] = True

    def get_edge(self, from_node: int, to_node: int) -> bool:
        return self._data[from_node][to_node]

    def get_connected(self, node: int) -> Iterator[int]:
        for i in range(self._size):
            if self._data[node][i]:
                yield i

    def get_connected_lst(self, node: int) -> List[int]:
        return list(self.get_connected(node))

    def inward_edges(self, node: int) -> Iterator[int]:
        for i in range(self._size):
            if self._data[i][node]:
                yield i

    def inward_edges_lst(self, node: int) -> List[int]:
        return list(self.inward_edges(node))

    # Compares two matrices
    def equals(self, other) -> bool:
        if self._size != other._size:
            return False
        for i in range(self._size):
            for j in range(self._size):
                if self.get_edge(i, j) != other.get_edge(i, j):
                    return False
        return True

    def subset(self, other) -> bool:
        if self._size != other._size:
            return False
        for i in range(self._size):
            for j in range(self._size):
                if other.get_edge(i, j) and not self.get_edge(i, j):
                    return False
        return True

    def size(self) -> int:
        return self._size
