
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

"""electrostatics.py - classes for electrostatics problems"""

import functools

import numpy
from numpy import array, arange, linspace, meshgrid, zeros_like, ones_like
from numpy import log10, sin, cos, arctan2, arccos, sqrt, fabs, cumsum
from numpy import radians, pi, infty
from numpy import dot, cross
from numpy import alltrue, isclose
from numpy import where, insert
from numpy import newaxis
from numpy.linalg import det

from scipy.integrate import ode
from scipy.interpolate import splrep, splev

import matplotlib
from matplotlib import pyplot

# The area of interest
XMIN, XMAX = None, None
YMIN, YMAX = None, None
ZOOM = None
XOFFSET = None


#-----------------------------------------------------------------------------
# Decorators

def arrayargs(func):
    """Ensures all args are arrays."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """Ensures all args are arrays."""
        # pylint: disable=star-args
        return func(*[array(a) for a in args], **kwargs)
    return wrapper


#-----------------------------------------------------------------------------
# Functions

# pylint: disable=too-many-arguments
def init(xmin, xmax, ymin, ymax, zoom=1, xoffset=0):
    """Initializes the domain."""
    # pylint: disable=global-statement
    global XMIN, XMAX, YMIN, YMAX, ZOOM, XOFFSET
    XMIN, XMAX, YMIN, YMAX, ZOOM, XOFFSET = \
      xmin, xmax, ymin, ymax, zoom, xoffset

def norm(x):
    """Returns the magnitude of the vector x."""
    return sqrt(numpy.sum(array(x)**2, axis=-1))

@arrayargs
def point_line_distance(x0, x1, x2):
    """Finds the shortest distance between the point x0 and the line x1 to x2.
    Ref: http://mathworld.wolfram.com/Point-LineDistance3-Dimensional.html"""
    assert x1.shape == x2.shape == (2,)
    return fabs(cross(x0-x1, x0-x2))/norm(x2-x1)

@arrayargs
def angle(x0, x1, x2):
    """Returns angle between three points.
    Ref: https://stackoverflow.com/questions/1211212"""
    assert x1.shape == x2.shape == (2,)
    a, b = x1 - x0, x1 - x2
    return arccos(dot(a, b)/(norm(a)*norm(b)))

@arrayargs
def is_left(x0, x1, x2):
    """Returns True if x0 is left of the line between x1 and x2,
    False otherwise.  Ref: https://stackoverflow.com/questions/1560492"""
    assert x1.shape == x2.shape == (2,)
    matrix = array([x1-x0, x2-x0])
    if len(x0.shape) == 2:
        matrix = matrix.transpose((1, 2, 0))
    return det(matrix) > 0

def lininterp2(x1, y1, x):
    """Linear interpolation at points x between numpy arrays (x1, y1).
    Only y1 is allowed to be two-dimensional.  The x1 values should be sorted
    from low to high.  Returns a numpy.array of y values corresponding to
    points x.
    """
    return splev(x, splrep(x1, y1, s=0, k=1))

def finalize_plot():
    """Finalizes the plot."""
    ax = pyplot.axes()
    ax.set_xticks([])
    ax.set_yticks([])
    pyplot.xlim(XMIN/ZOOM+XOFFSET, XMAX/ZOOM+XOFFSET)
    pyplot.ylim(YMIN/ZOOM, YMAX/ZOOM)
    pyplot.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)


#-----------------------------------------------------------------------------
# Classes

class PointCharge:
    """A point charge."""

    R = 0.01  # The effective radius of the charge

    def __init__(self, q, x):
        """Initializes the quantity of charge 'q' and position vector 'x'."""
        self.q, self.x = q, array(x)

    def E(self, x):  # pylint: disable=invalid-name
        """Electric field vector."""
        if self.q == 0:
            return 0
        else:
            dx = x-self.x
            return (self.q*dx.T/numpy.sum(dx**2, axis=-1)**1.5).T

    def V(self, x):  # pylint: disable=invalid-name
        """Potential."""
        return self.q/norm(x-self.x)

    def is_close(self, x):
        """Returns True if x is close to the charge; false otherwise."""
        return norm(x-self.x) < self.R

    def plot(self):
        """Plots the charge."""
        color = 'b' if self.q < 0 else 'r' if self.q > 0 else 'k'
        r = 0.1*(sqrt(fabs(self.q))/2 + 1)
        circle = pyplot.Circle(self.x, r, color=color, zorder=10)
        pyplot.gca().add_artist(circle)


class PointChargeFlatland(PointCharge):
    """A point charge in Flatland.
    Ref: https://physics.stackexchange.com/questions/44515"""

    def E(self, x):  # pylint: disable=invalid-name
        """Electric field vector."""
        dx = x-self.x
        return (self.q*dx.T/numpy.sum(dx**2, axis=-1)).T

    def V(self, x):
        raise RuntimeError('Not implemented')


class LineCharge:
    """A line charge."""

    R = 0.01  # The effective radius of the charge

    def __init__(self, q, x1, x2):
        """Initializes the quantity of charge 'q' and end point vectors
        'x1' and 'x2'."""
        self.q, self.x1, self.x2 = q, array(x1), array(x2)

    def get_lam(self):
        """Returns the total charge on the line."""
        return self.q / norm(self.x2 - self.x1)
    lam = property(get_lam)

    def E(self, x):  # pylint: disable=invalid-name
        """Electric field vector.
        Ref: http://www.phys.uri.edu/gerhard/PHY204/tsl31.pdf
        """
        x = array(x)
        x1, x2, lam = self.x1, self.x2, self.lam

        # Get lengths and angles for the different triangles
        theta1, theta2 = angle(x, x1, x2), pi - angle(x, x2, x1)
        a = point_line_distance(x, x1, x2)
        r1, r2 = norm(x - x1), norm(x - x2)

        # Calculate the parallel and perpendicular components
        sign = where(is_left(x, x1, x2), 1, -1)

        # pylint: disable=invalid-name
        Epara = lam*(1/r2-1/r1)
        Eperp = -sign*lam*(cos(theta2)-cos(theta1))/where(a == 0, infty, a)

        # Transform into the coordinate space and return
        dx = x2 - x1

        if len(x.shape) == 2:
            Epara = Epara[::, newaxis]
            Eperp = Eperp[::, newaxis]

        return Eperp * (array([-dx[1], dx[0]])/norm(dx)) + Epara * (dx/norm(dx))

    def is_close(self, x):
        """Returns True if x is close to the charge."""

        theta1 = angle(x, self.x1, self.x2)
        theta2 = angle(x, self.x2, self.x1)

        if theta1 < radians(90) and theta2 < radians(90):
            return point_line_distance(x, self.x1, self.x2) < self.R
        else:
            return numpy.min([norm(self.x1-x), norm(self.x2-x)], axis=0) < \
              self.R

    def plot(self):
        """Plots the charge."""
        color = 'b' if self.q < 0 else 'r' if self.q > 0 else 'k'
        x, y = zip(self.x1, self.x2)
        width = 5*(sqrt(fabs(self.lam))/2 + 1)
        pyplot.plot(x, y, color, linewidth=width)


# pylint: disable=too-few-public-methods
class FieldLine:
    """A Field Line."""

    def __init__(self, x):
        "Initializes the field line points 'x'."""
        self.x = x

    def plot(self, linewidth=None, startarrows=True, endarrows=True):
        """Plots the field line and arrows."""

        if linewidth == None:
            linewidth = matplotlib.rcParams['lines.linewidth']
        
        x, y = zip(*self.x)
        pyplot.plot(x, y, '-k', linewidth=linewidth)

        n = int(len(x)/2) if len(x) < 225 else 75
        if startarrows:
            pyplot.arrow(x[n], y[n], (x[n+1]-x[n])/100., (y[n+1]-y[n])/100.,
                         fc="k", ec="k",
                         head_width=0.1*linewidth, head_length=0.1*linewidth)

        if len(x) < 225 or not endarrows:
            return

        pyplot.arrow(x[-n], y[-n],
                     (x[-n+1]-x[-n])/100., (y[-n+1]-y[-n])/100.,
                     fc="k", ec="k",
                     head_width=0.1*linewidth, head_length=0.1*linewidth)


class ElectricField:
    """The electric field owing to a collection of charges."""

    dt0 = 0.01  # The time step for integrations

    def __init__(self, charges):
        """Initializes the field given 'charges'."""
        self.charges = charges

    def vector(self, x):
        """Returns the field vector."""
        return numpy.sum([charge.E(x) for charge in self.charges], axis=0)

    def magnitude(self, x):
        """Returns the magnitude of the field vector."""
        return norm(self.vector(x))

    def angle(self, x):
        """Returns the field vector's angle from the x-axis (in radians)."""
        return arctan2(*(self.vector(x).T[::-1])) # arctan2 gets quadrant right

    def direction(self, x):
        """Returns a unit vector pointing in the direction of the field."""
        v = self.vector(x)
        return (v.T/norm(v)).T

    def projection(self, x, a):
        """Returns the projection of the field vector on a line at given angle
        from x-axis."""
        return self.magnitude(x) * cos(a - self.angle(x))

    def line(self, x0):
        """Returns the field line passing through x0.
        Refs: http://folk.uib.no/fcihh/seminar/lec1.pdf and lect2.pdf
              http://numbercrunch.de/blog/2013/05/visualizing-streamlines/
        and especially: "Electric field lines don't work",
        http://scitation.aip.org/content/aapt/journal/ajp/64/6/10.1119/1.18237
        """

        if None in [XMIN, XMAX, YMIN, YMAX]:
            raise ValueError('Domain must be set using init().')

        # Set up integrator for the field line
        streamline = lambda t, y: list(self.direction(y))
        solver = ode(streamline).set_integrator('vode')

        # Initialize the coordinate lists
        x = [x0]

        # Integrate in both the forward and backward directions
        dt = 0.008

        # Solve in both the forward and reverse directions
        for sign in [1, -1]:

            # Set the starting coordinates and time
            solver.set_initial_value(x0, 0)

            # Integrate field line over successive time steps
            while solver.successful():

                # Find the next step
                solver.integrate(solver.t + sign*dt)

                # Save the coordinates
                if sign > 0:
                    x.append(solver.y)
                else:
                    x.insert(0, solver.y)

                # Check if line connects to a charge
                flag = False
                for c in self.charges:
                    if c.is_close(solver.y):
                        flag = True
                        break

                # Terminate line at charge or if it leaves the area of interest
                if flag or not (XMIN < solver.y[0] < XMAX) or \
                  not YMIN < solver.y[1] < YMAX:
                    break

        return FieldLine(x)

    def plot(self, nmin=-3.5, nmax=1.5):
        """Plots the field magnitude."""
        x, y = meshgrid(
            linspace(XMIN/ZOOM+XOFFSET, XMAX/ZOOM+XOFFSET, 200),
            linspace(YMIN/ZOOM, YMAX/ZOOM, 200))
        z = zeros_like(x)
        for i in range(x.shape[0]):
            for j in range(x.shape[1]):
                z[i, j] = log10(self.magnitude([x[i, j], y[i, j]]))
        levels = arange(nmin, nmax+0.2, 0.2)
        cmap = pyplot.cm.get_cmap('plasma')
        pyplot.contourf(x, y, numpy.clip(z, nmin, nmax),
                        10, cmap=cmap, levels=levels, extend='both')


# pylint: disable=too-few-public-methods
class GaussianCircle:
    """A Gaussian circle with radius r."""

    def __init__(self, x, r, a0=0):
        """Initializes the Gaussian surface at position vector 'x'
        and given radius 'r'.  'a0' defines an offset angle CCW from the
        x-axis.  Use this to identify the axis around which flux points should
        be symmetric."""
        self.x = x
        self.r = r
        self.a0 = a0

    def fluxpoints(self, field, n, uniform=False):
        """Returns points where field lines should enter/exit the surface.

        The flux points are usually chosen so that they are equally separated
        in electric field flux.  However, if 'uniform' is True then the points
        are equispaced.

        This method requires that the flux be in xor out everywhere on the
        circle (unless 'uniform' is True)."""

        # Create a dense array of points around the circle
        a = radians(linspace(0, 360, 1001)) + self.a0
        assert len(a)%4 == 1
        x = self.r*array([cos(a), sin(a)]).T + self.x

        if uniform:
            flux = ones_like(a)

        else:
            # Get the flux through each point.  Ensure the fluxes are either
            # all in or all out.
            flux = field.projection(x, a)

            if numpy.sum(flux) < 0:
                flux *= -1
            assert alltrue(flux > 0)

        # Create an integrated flux curve
        intflux = insert(cumsum((flux[:-1]+flux[1:])/2), 0, 0)
        assert isclose(intflux[-1], numpy.sum(flux[:-1]))

        # Divide the integrated flux curve into n+1 portions, and calculate
        # the corresponding angles.
        v = linspace(0, intflux[-1], n+1)
        a = lininterp2(intflux, a, v)[:-1]

        return self.r*array([cos(a), sin(a)]).T + self.x


