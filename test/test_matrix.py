from unittest import TestCase
from colouring.matrix import Matrix

class TestMatrix(TestCase):
    def test_create_matrix_size(self):
        m = Matrix(size = 3)
        assert m.size() == 3

    def test_add_edge(self):
        m = Matrix(size = 3)
        m.add_edge(0, 1)
        assert m.get_edge(0, 1)

    def test_connected(self):
        m = Matrix(size = 3)
        m.add_edge(0, 1)
        assert 1 in m.get_connected_lst(0)

    def test_equal(self):
        a = Matrix(size = 3)
        a.add_edge(0, 1)
        b = Matrix(size = 3)
        b.add_edge(1, 0)

        assert not a.equals(b)

    def test_equal_size(self):
        a = Matrix(size = 3)
        a.add_edge(0, 1)
        b = Matrix(size = 4)
        b.add_edge(0, 1)

        assert not a.equals(b)
