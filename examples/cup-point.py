#!/usr/bin/env python3

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

"""Plots field lines for a cup and point charge."""

from matplotlib import pyplot
import electrostatics
from electrostatics import PointCharge, LineCharge
from electrostatics import ElectricField, GaussianCircle
from electrostatics import finalize_plot

# pylint: disable=invalid-name

XMIN, XMAX = -200, 200
YMIN, YMAX = -150, 150
ZOOM = 30
XOFFSET = 0

electrostatics.init(XMIN, XMAX, YMIN, YMAX, ZOOM, XOFFSET)

# Set up the charges and electric field
charges = [LineCharge(0.2, [-2, -0.5], [-2, 0.5]),
           LineCharge(0.4, [-2, -0.5], [0, -0.5]),
           LineCharge(0.4, [-2, 0.5], [0, 0.5]),
           PointCharge(-1, [1, 0])]
field = ElectricField(charges)

# Set up the Gaussian surfaces
g = GaussianCircle(charges[-1].x, 0.1)

# Create the field lines
fieldlines = []
for x in g.fluxpoints(field, 15):
    fieldlines.append(field.line(x))
fieldlines.append(field.line([-3, 0]))

# Plotting
fig = pyplot.figure(figsize=(6, 4.5))
field.plot()
for fieldline in fieldlines:
    fieldline.plot()
for charge in charges:
    charge.plot()
finalize_plot()
pyplot.show()
