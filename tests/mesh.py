import unittest

import numpy

from src.core import Triangle, Mesh


class MeshTest(unittest.TestCase):
    def test_something(self):
        vertex_one: numpy.ndarray = numpy.array([0, 0, 0], dtype=int)
        vertex_two: numpy.ndarray = numpy.array([0, 1, 0], dtype=int)
        vertex_three: numpy.ndarray = numpy.array([0, 0, 1], dtype=int)
        test_triangle: Triangle = Triangle(vertices=[vertex_one, vertex_two, vertex_three])
        test_mesh: Mesh = Mesh(vertex_order=[test_triangle])
        boundary_box: tuple[numpy.ndarray, numpy.ndarray] = test_mesh.boundary_box

        self.assertTrue(isinstance(test_mesh.triangles, list))
        self.assertTrue(isinstance(test_mesh.triangles[0], Triangle))
        self.assertEqual(boundary_box[0].all(), numpy.array([0, 0, 0], dtype=int).all())
        self.assertEqual(boundary_box[1].all(), numpy.array([0, 1, 1], dtype=int).all())
