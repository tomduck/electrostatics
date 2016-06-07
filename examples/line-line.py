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

"""Plots field lines for two line charges."""

from matplotlib import pyplot
import numpy

import electrostatics
from electrostatics import LineCharge
from electrostatics import ElectricField
from electrostatics import finalize_plot

# pylint: disable=invalid-name

XMIN, XMAX = -40, 40
YMIN, YMAX = -30, 30
ZOOM = 5
XOFFSET = 0

electrostatics.init(XMIN, XMAX, YMIN, YMAX, ZOOM, XOFFSET)

# Set up the charges and electric field
a = 3
charges = [LineCharge(1, [-0.5, -a], [-0.5, a]),
           LineCharge(-1, [0.5, -a], [0.5, a])]
field = ElectricField(charges)

# Create the flux points manually
fluxpoints = []
fluxpoints += list([-0.51, y] for y in numpy.linspace(-a, a, 9)[1:-1])
fluxpoints += list([-0.49, y] for y in numpy.linspace(-a, a, 9)[1:-1])
fluxpoints += [[-0.5, -a-0.01], [-0.5, a+0.01]]

# Create the field lines
fieldlines = []
for x in fluxpoints:
    fieldlines.append(field.line(x))
fieldlines.append(field.line([10, 0]))

# Plotting
fig = pyplot.figure(figsize=(6, 4.5))
field.plot()
for fieldline in fieldlines:
    fieldline.plot()
for charge in charges:
    charge.plot()
finalize_plot()
pyplot.show()

