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

"""Plots field lines for dipole."""

from matplotlib import pyplot
import numpy

import electrostatics
from electrostatics import PointCharge, ElectricField, GaussianCircle
from electrostatics import finalize_plot

# pylint: disable=invalid-name

XMIN, XMAX = -40, 40
YMIN, YMAX = -30, 30
ZOOM = 6
XOFFSET = 0

electrostatics.init(XMIN, XMAX, YMIN, YMAX, ZOOM, XOFFSET)

# Set up the charges and electric field
charges = [PointCharge(1, [-1, 0]),
           PointCharge(-1, [1, 0])]
field = ElectricField(charges)

# Set up the Gaussian surfaces
g = GaussianCircle(charges[0].x, 0.1)

# Create the field lines
fieldlines = []
for x in g.fluxpoints(field, 12):
    fieldlines.append(field.line(x))
fieldlines.append(field.line([10, 0]))

# Create the vector grid
x, y = numpy.meshgrid(numpy.linspace(XMIN/ZOOM+XOFFSET, XMAX/ZOOM+XOFFSET, 28),
                      numpy.linspace(YMIN/ZOOM, YMAX/ZOOM, 18))
u, v = numpy.zeros_like(x), numpy.zeros_like(y)
n, m = x.shape
scale = 1/field.magnitude([XMIN/ZOOM+XOFFSET, YMIN/ZOOM])
for i in range(n):
    for j in range(m):
        mag = numpy.log10(field.magnitude([x[i, j], y[i, j]])*scale)
        a = field.angle([x[i, j], y[i, j]])
        u[i, j], v[i, j] = mag*numpy.cos(a), mag*numpy.sin(a)


## Plotting ##

# Field lines
pyplot.figure(figsize=(6, 4.5))
field.plot()
for fieldline in fieldlines:
    fieldline.plot()
for charge in charges:
    charge.plot()
finalize_plot()

# Field vectors
pyplot.figure(figsize=(6, 4.5))
cmap = pyplot.cm.get_cmap('plasma')
pyplot.quiver(x, y, u, v, mag, pivot='mid', cmap=cmap, scale=75)
for charge in charges:
    charge.plot()
finalize_plot()

pyplot.show()
