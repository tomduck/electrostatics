#! /usr/bin/env python3

"""Unit tests for electrostatics.py."""

# Copyright 2016 Thomas J. Duck.
# All rights reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest
import sys

from numpy import array, sqrt, cos, fabs, radians, isclose, append

from electrostatics import norm, point_line_distance, angle, is_left
from electrostatics import PointCharge, PointChargeFlatland, LineCharge
from electrostatics import ElectricField, GaussianCircle

# pylint: disable=invalid-name

#-----------------------------------------------------------------------------
# Unit test classes

class TestFunctions(unittest.TestCase):
    """Tests functions in the electrostatics module."""

    def test_norm(self):
        """Tests norm()."""
        self.assertEqual(norm([1, 0]), 1)
        self.assertTrue((norm([[1, 0], [2, 0]]) == [1, 2]).all())

    def test_point_line_distance(self):
        """Tests point_line_distance()."""
        x1, x2 = [-1, 1], [0, 0]
        self.assertEqual(point_line_distance([2, -1], x1, x2), 1/sqrt(2))
        self.assertEqual(point_line_distance([0, 0], x1, x2), 0)
        self.assertEqual(point_line_distance([-2, 1], x1, x2), 1/sqrt(2))
        self.assertTrue(
            (point_line_distance([[2, -1], [0, 0], [-2, 1]], x1, x2) ==
             [1/sqrt(2), 0, 1/sqrt(2)]).all())

    def test_angle(self):
        """Tests angle()."""
        x1, x2 = [0, 0], [1, 0]
        self.assertTrue(isclose(angle([1, 1], x1, x2), radians(45)))
        self.assertTrue(isclose(angle([0, 1], x1, x2), radians(90)))
        self.assertTrue(isclose(angle([-1, 1], x1, x2), radians(135)))
        self.assertTrue(isclose(angle([[1, 1], [0, 1], [-1, 1]], x1, x2),
                                [radians(45), radians(90), radians(135)]).all())

    def test_is_left(self):
        """Tests is_left()."""

        x1, x2 = [0, 0], [1, 0]
        self.assertTrue(is_left([0, 1], x1, x2))
        self.assertFalse(is_left([0, -1], x1, x2))
        self.assertFalse(is_left([2, 0], x1, x2))
        self.assertTrue((is_left([[0, 1], [0, -1], [2, 0]], x1, x2) ==
                         [True, False, False]).all())

        x1, x2 = [0, 0], [1, 1]
        self.assertTrue(is_left([0, 1], x1, x2))
        self.assertFalse(is_left([0, -1], x1, x2))
        self.assertFalse(is_left([2, 2], x1, x2))
        self.assertTrue((is_left([[0, 1], [0, -1], [2, 2]], x1, x2) ==
                         [True, False, False]).all())


class TestPointCharge(unittest.TestCase):
    """Tests the PointCharge class."""

    def setUp(self):
        """Creates a q=2 point charge  at (0, 0)."""
        self.charge = PointCharge(2, [0, 0])

    def test_E(self):
        """Tests the electric field."""
        E = self.charge.E
        self.assertTrue((E([1, 0]) == [2, 0]).all())
        self.assertTrue((E([2, 0]) == [0.5, 0]).all())
        self.assertTrue((E([1, 1]) == [1/sqrt(2), 1/sqrt(2)]).all())
        self.assertTrue((E([[1, 0], [2, 0], [1, 1]]) ==
                         [[2, 0], [0.5, 0], [1/sqrt(2), 1/sqrt(2)]]).all())

    def test_V(self):
        """Tests the potential."""
        V = self.charge.V
        self.assertEqual(V([1, 0]), 2)
        self.assertEqual(V([2, 0]), 1)
        self.assertTrue(isclose(V([1, 1]), sqrt(2)))
        self.assertTrue(isclose(V([[1, 0], [2, 0], [1, 1]]),
                                [2, 1, sqrt(2)]).all())


class TestPointChargeFlatland(unittest.TestCase):
    """Tests the PointChargeFlatland class."""

    def setUp(self):
        """Creates a q=2 point charge  at (0, 0)."""
        self.charge = PointChargeFlatland(2, [0, 0])

    def test_E(self):
        """Tests the electric field."""
        E = self.charge.E
        self.assertTrue((E([1, 0]) == [2, 0]).all())
        self.assertTrue((E([2, 0]) == [1, 0]).all())
        self.assertTrue((E([1, 1]) == [1, 1]).all())
        self.assertTrue((E([[1, 0], [2, 0], [1, 1]]) ==
                         [[2, 0], [1, 0], [1, 1]]).all())

    def test_V(self):
        """Tests the potential."""
        pass


class TestLineCharge(unittest.TestCase):
    """Tests the LineCharge class."""

    def setUp(self):
        """Creates a line charge2."""
        self.charge1a = LineCharge(2, [-1, 0], [1, 0])
        self.charge1b = LineCharge(2, [1, 0], [-1, 0])
        self.charge2 = LineCharge(6, [0, -1], [0, 1])

    def test_q(self):
        """Tests the total charge."""
        self.assertEqual(self.charge1a.q, 2)
        self.assertEqual(self.charge1b.q, 2)
        self.assertEqual(self.charge2.q, 6)

    def test_E_1(self):
        """Tests the electric field 1."""
        for E in [self.charge1a.E, self.charge1b.E]:
            self.assertTrue(isclose(E([0, 1]), [0, sqrt(2)]).all())
            self.assertTrue(isclose(E([0, -1]), [0, -sqrt(2)]).all())
            self.assertTrue(isclose(E([1, 2]),
                                    array([1-1/sqrt(2), 1/sqrt(2)])/2).all())
            self.assertTrue(isclose(E([1, -2]),
                                    array([1-1/sqrt(2), -1/sqrt(2)])/2).all())
            self.assertTrue(isclose(E([-1, 2]),
                                    array([-1+1/sqrt(2), 1/sqrt(2)])/2).all())
            self.assertTrue(isclose(E([-1, -2]),
                                    array([-1+1/sqrt(2), -1/sqrt(2)])/2).all())
            self.assertTrue(isclose(E([2, 0]), [2/3, 0]).all())
            self.assertTrue(isclose(E([-2, 0]), [-2/3, 0]).all())
            self.assertTrue(isclose(E([[0, 1], [0, -1], [1, 2]]),
                                    [[0, sqrt(2)],
                                     [0, -sqrt(2)],
                                     array([1-1/sqrt(2), 1/sqrt(2)])/2]).all())

    def test_E_2(self):
        """Tests the electric field 2."""
        E = self.charge2.E
        self.assertTrue(isclose(E([1, 0]), [3*sqrt(2), 0]).all())
        self.assertTrue(isclose(E([-1, 0]), [-3*sqrt(2), 0]).all())
        self.assertTrue(isclose(E([2, 1]),
                                array([1/sqrt(2), 1-1/sqrt(2)])*1.5).all())
        self.assertTrue(isclose(E([-2, 1]),
                                array([-1/sqrt(2), 1-1/sqrt(2)])*1.5).all())
        self.assertTrue(isclose(E([2, -1]),
                                array([1/sqrt(2), -1+1/sqrt(2)])*1.5).all())
        self.assertTrue(isclose(E([-2, -1]),
                                array([-1/sqrt(2), -1+1/sqrt(2)])*1.5).all())

        self.assertTrue(isclose(E([0, 2]), [0, 2]).all())
        self.assertTrue(isclose(E([0, -2]), [0, -2]).all())


class TestElectricField(unittest.TestCase):
    """Tests the ElectricField class."""

    def setUp(self):
        """Sets up a dipole centred at (0, 0)."""
        charges = [PointCharge(-2, [-1, 0]), PointCharge(2, [1, 0])]
        self.field = ElectricField(charges)

    def test_vector(self):
        """Tests the electric field vector."""
        vector = self.field.vector
        self.assertTrue((vector([0, 0]) == [-4, 0]).all())
        self.assertTrue((vector([3, 0]) == [0.375, 0]).all())
        self.assertTrue(isclose(vector([0, 1]), [-sqrt(2), 0]).all())
        self.assertTrue(isclose(vector([[0, 0], [3, 0], [0, 1]]),
                                [[-4, 0], [0.375, 0], [-sqrt(2), 0]]).all())

    def test_magnitude(self):
        """Tests the electric field magnitude."""
        magnitude = self.field.magnitude
        self.assertTrue(magnitude([0, 0]) == 4)
        self.assertTrue(magnitude([3, 0]) == 0.375)
        self.assertTrue(isclose(magnitude([0, 1]), sqrt(2)))
        self.assertTrue(isclose(magnitude([[0, 0], [3, 0], [0, 1]]),
                                [4, 0.375, sqrt(2)]).all())

    def test_angle(self):
        """Tests the electric field angle."""
        a = self.field.angle
        self.assertTrue(a([0, 0]) == radians(180))
        self.assertTrue(a([3, 0]) == 0)
        self.assertTrue(a([0, 1]) == radians(180))
        self.assertTrue((a([[0, 0], [3, 0], [0, 1]]) ==
                         [radians(180), 0, radians(180)]).all())

    def test_direction(self):
        """Tests the electric field direction."""
        direction = self.field.direction
        self.assertTrue((direction([0, 0]) == [-1, 0]).all())
        self.assertTrue((direction([3, 0]) == [1, 0]).all())
        self.assertTrue((direction([0, 1]) == [-1, 0]).all())
        self.assertTrue((direction([[0, 0], [3, 0], [0, 1]]) ==
                         [[-1, 0], [1, 0], [-1, 0]]).all())

    def test_projection(self):
        """Tests the electric field projection."""

        projection = self.field.projection

        # Top-right quadrant
        a = radians(45)
        self.assertTrue(isclose(projection([0, 0], a), -4*cos(a)))
        self.assertTrue(isclose(projection([3, 0], a), 0.375*cos(a)))
        self.assertTrue(isclose(projection([0, 1], a), -sqrt(2)*cos(a)))
        self.assertTrue(isclose(projection([[0, 0], [3, 0], [0, 1]], a),
                                array([-4, 0.375, -sqrt(2)])*cos(a)).all())


        # Bottom-left quadrant
        a1 = radians(-135)
        a2 = radians(45)
        self.assertTrue(isclose(projection([0, 0], a1), 4*cos(a2)))
        self.assertTrue(isclose(projection([3, 0], a1), -0.375*cos(a2)))
        self.assertTrue(isclose(projection([0, 1], a1),
                                sqrt(2)*cos(a2)))
        self.assertTrue(isclose(projection([[0, 0], [3, 0], [0, 1]], a1),
                                array([4, -0.375, sqrt(2)])*cos(a2)).all())


class TestGaussianCircle(unittest.TestCase):
    """Tests the GaussianCircle class."""

    def setUp(self):
        """Creates a Gaussian circle around a q=2 point charge  at (0, 0)."""

    def test_monopole_fluxpoints(self):
        """Tests monopole flux points."""

        field = ElectricField([PointCharge(2, [0, 0])])
        circle = GaussianCircle([0, 0], 10)

        fluxpoints = circle.fluxpoints(field, 4)
        self.assertEqual(len(fluxpoints), 4)
        self.assertTrue(isclose(fluxpoints,
                                [[10, 0], [0, 10], [-10, 0], [0, -10]]).all())

        fluxpoints = circle.fluxpoints(field, 14)
        self.assertEqual(len(fluxpoints), 14)
        self.assertTrue(isclose(fluxpoints[0], [10, 0]).all())
        self.assertTrue(isclose(fluxpoints[7], [-10, 0]).all())

        x1 = fluxpoints[1:7]
        x2 = fluxpoints[-1:7:-1]
        x2[:, 1] = fabs(x2[:, 1])
        self.assertTrue(isclose(x1, x2).all())

        x1 = append(fluxpoints[-3:], fluxpoints[:4], axis=0)
        x2 = fluxpoints[-4:3:-1]
        x2[:, 0] = fabs(x2[:, 0])
        self.assertEqual(len(x1), len(x2))
        self.assertTrue(isclose(x1, x2).all())

    def test_dipole_fluxpoints(self):
        """Tests dipole flux points."""

        field = ElectricField([PointCharge(-2, [0, 0]), PointCharge(2, [2, 0])])
        circle = GaussianCircle([0, 0], 0.1)

        fluxpoints = circle.fluxpoints(field, 4)
        self.assertEqual(len(fluxpoints), 4)

        fluxpoints = circle.fluxpoints(field, 14)
        self.assertEqual(len(fluxpoints), 14)
        self.assertTrue(isclose(fluxpoints[0], [0.1, 0]).all())
        self.assertTrue(isclose(fluxpoints[7], [-0.1, 0]).all())

        x1 = fluxpoints[1:7]
        x2 = fluxpoints[-1:7:-1]
        x2[:, 1] = fabs(x2[:, 1])
        self.assertTrue(isclose(x1, x2).all())


#-----------------------------------------------------------------------------
# main()

def main():
    """Runs the unit tests"""

    suite = unittest.TestSuite()

    suite.addTests(unittest.makeSuite(TestFunctions))
    suite.addTests(unittest.makeSuite(TestPointCharge))
    suite.addTests(unittest.makeSuite(TestLineCharge))
    suite.addTests(unittest.makeSuite(TestElectricField))
    suite.addTests(unittest.makeSuite(TestGaussianCircle))

    result = unittest.TextTestRunner(verbosity=1).run(suite)

    n_errors = len(result.errors)
    n_failures = len(result.failures)

    if n_errors or n_failures:
        print('\n\nSummary: %d errors and %d failures reported\n'%\
            (n_errors, n_failures))

    print()

    sys.exit(n_errors+n_failures)


if __name__ == '__main__':
    main()
