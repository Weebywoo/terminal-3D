import unittest

import numpy

from src.triangle import Triangle


class TriangleTest(unittest.TestCase):
    def test_triangle_vertex_access(self):
        vertex_one: numpy.ndarray = numpy.array([0, 0, 0], dtype=int)
        vertex_two: numpy.ndarray = numpy.array([0, 1, 0], dtype=int)
        vertex_three: numpy.ndarray = numpy.array([0, 0, 1], dtype=int)
        test_triangle: Triangle = Triangle(vertices=[vertex_one, vertex_two, vertex_three])

        self.assertTrue(hasattr(test_triangle, "__getitem__"))
        self.assertEqual(test_triangle[0].all(), vertex_one.all())
        self.assertEqual(test_triangle[1].all(), vertex_two.all())
        self.assertEqual(test_triangle[2].all(), vertex_three.all())
