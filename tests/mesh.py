import unittest

import numpy

from src.mesh import Mesh


class MeshTest(unittest.TestCase):
    def test_something(self):
        vertex_one: numpy.ndarray = numpy.array([0, 0, 0], dtype=int)
        vertex_two: numpy.ndarray = numpy.array([0, 1, 0], dtype=int)
        vertex_three: numpy.ndarray = numpy.array([0, 0, 1], dtype=int)
        test_mesh: Mesh = Mesh(vertices=[vertex_one, vertex_two, vertex_three], vertex_order=[0, 1, 2])
        boundary_box: tuple[numpy.ndarray, numpy.ndarray] = test_mesh.boundary_box

        self.assertTrue(isinstance(test_mesh, list))
        self.assertTrue(isinstance(test_mesh[0], tuple))
        self.assertEqual(test_mesh[0], (vertex_one, vertex_two, vertex_three))
        self.assertEqual(boundary_box[0].all(), numpy.array([0, 0, 0], dtype=int).all())
        self.assertEqual(boundary_box[1].all(), numpy.array([0, 1, 1], dtype=int).all())
