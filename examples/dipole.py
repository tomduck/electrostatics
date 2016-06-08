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

# Set up the Gaussian surface
g = GaussianCircle(charges[0].x, 0.1)

# Create the field lines
fieldlines = []
for x in g.fluxpoints(field, 12):
    fieldlines.append(field.line(x))
fieldlines.append(field.line([10, 0]))

# Create the vector grid
x, y = numpy.meshgrid(numpy.linspace(XMIN/ZOOM+XOFFSET, XMAX/ZOOM+XOFFSET, 41),
                      numpy.linspace(YMIN/ZOOM, YMAX/ZOOM, 31))
u, v = numpy.zeros_like(x), numpy.zeros_like(y)
n, m = x.shape
for i in range(n):
    for j in range(m):
        if any(numpy.isclose(electrostatics.norm(charge.x-[x[i, j], y[i, j]]),
                             0) for charge in charges):
            u[i, j] = v[i, j] = None
        else:
            mag = field.magnitude([x[i, j], y[i, j]])**(1/5)
            a = field.angle([x[i, j], y[i, j]])
            u[i, j], v[i, j] = mag*numpy.cos(a), mag*numpy.sin(a)

## Plotting ##

# Field lines
fig = pyplot.figure(figsize=(6, 4.5))
field.plot()
for fieldline in fieldlines:
    fieldline.plot()
for charge in charges:
    charge.plot()
finalize_plot()
#fig.savefig('dipole-field-lines.pdf', transparent=True)

# Field vectors
fig = pyplot.figure(figsize=(6, 4.5))
cmap = pyplot.cm.get_cmap('plasma')
pyplot.quiver(x, y, u, v, pivot='mid', cmap=cmap, scale=35)
for charge in charges:
    charge.plot()
finalize_plot()
#fig.savefig('dipole-field-vectors.pdf', transparent=True)

pyplot.show()
