
electrostatics 0.2.0
====================

*electrostatics.py* is a python module for electrostatics field and potential calculations, and field line and equipotential contour plots.


Installation
------------

Install into python by executing

~~~
# pip install git+https://github.com/tomduck/electrostatics.git --user
~~~


Examples
--------

Textbook examples are given below along with a selection of cases from the excellent [paper] "Electric field lines don't work" by Wolf, Van Hook and Weeks (*Am. J. Phys., 64,* 1996).  Solid lines are the field lines, dotted lines are equipotential contours, and colours give the field strength.

In each case field lines are initialized symmetrically close to one (or more) charges.  Paths are determined numerically from the [streamline equation] using an ODE solver.  The integration parameters were adapted from Heiko Bauke's [page] on "Visualizing Streamlines".

The colours in each image give the logarithm of the field magnitude.  Each colour step represents a 0.2 change in log-10 space (5 steps represents a decade).  The field in close proximity to a charge is clipped to a maximum value.

[paper]: http://scitation.aip.org/content/aapt/journal/ajp/64/6/10.1119/1.18237

[streamline equation]: http://folk.uib.no/fcihh/seminar/lec1.pdf

[page]: http://numbercrunch.de/blog/2013/05/visualizing-streamlines/


### Dipole ###

The left charge is +1 and the right charge is -1.  In textbook examples like this the lines are symmetrically distributed around each charge no matter which charge they are initialized around.

![Dipole.](https://raw.githubusercontent.com/tomduck/electrostatics/master/images/dipole.png)

Below is the corresponding electric field vector plot.  The length of the vectors is the fifth root of the electric field magnitude.   The field line diagrams make visualizing the field much easier.

![Dipole vectors.](https://raw.githubusercontent.com/tomduck/electrostatics/master/images/dipole-vectors.png)

[Source.](https://github.com/tomduck/electrostatics/blob/master/examples/dipole.py)


### Biased Dipole ###

The left charge is +2 and the right charge -1.  Field lines are initialized symmetrically around the -1 charge, and again symmetrically in the far field.  Notice that the +2 charge exhibits "equatorial clumping" of the field lines, and that there is divergence from the zero-field point (in black).  Equatorial clumping and 2D divergence are artefacts that arise from taking a 2D slice of a 3D field.

![Biased dipole.](https://raw.githubusercontent.com/tomduck/electrostatics/master/images/biased-dipole.png)

[Source.](https://github.com/tomduck/electrostatics/blob/master/examples/biased-dipole.py)


### Biased Dipole in Flatland ###

This example is for a theoretical electric field that is non-divergent in 2D (i.e., [Flatland]).  There is no clumping and the zero-field point has the same number of lines entering and leaving it, as expected.

[Flatland]: https://en.wikipedia.org/wiki/Flatland

![Biased dipole in Flatland.](https://raw.githubusercontent.com/tomduck/electrostatics/master/images/biased-dipole-flatland.png)

[Source.](https://github.com/tomduck/electrostatics/blob/master/examples/biased-dipole-flatland.py)


### Two Positive Charges ###

This is another textbook example.  Note the equatorial clumping in the far field and the point of 2D convergence in the middle.

![Two positive charges.](https://raw.githubusercontent.com/tomduck/electrostatics/master/images/two-positive-charges.png)

[Source.](https://github.com/tomduck/electrostatics/blob/master/examples/two-positive-charges.py)


### Line - Point ###

Both the line and point have the same amount of charge.  Lines are initialized symmetrically around the point charge.  That they do not connect to the line symmetrically is a 2D slice artefact.

![Line - point.](https://raw.githubusercontent.com/tomduck/electrostatics/master/images/line-point.png)

[Source.](https://github.com/tomduck/electrostatics/blob/master/examples/line-point.py)


### Line - Line ###

The lines are initialized symmetrically close to one line and connect to the other symmetrically, as expected.

![Line - line.](https://raw.githubusercontent.com/tomduck/electrostatics/master/images/line-line.png)

[Source.](https://github.com/tomduck/electrostatics/blob/master/examples/line-line.py)


### Cup - Point ###

The cup and point have equal and opposite charges.  Note that few field lines enter the cup.

![Cup - point.](https://raw.githubusercontent.com/tomduck/electrostatics/master/images/cup-point.png)

[Source.](https://github.com/tomduck/electrostatics/blob/master/examples/cup-point.py)


### Quadrupole ###

Another textbook example with perfect symmetry.

![Quadrupole.](https://raw.githubusercontent.com/tomduck/electrostatics/master/images/quadrupole.png)

[Source.](https://github.com/tomduck/electrostatics/blob/master/examples/quadrupole.py)


### Linear Quadrupole ###

The middle charge is -4 and the outer charges are +2.  Lines are initialized symmetrically around the positive charges.  Note the equatorial clumping around the negative charge.

![Linear quadrupole.](https://raw.githubusercontent.com/tomduck/electrostatics/master/images/linear-quadrupole.png)

[Source.](https://github.com/tomduck/electrostatics/blob/master/examples/linear-quadrupole.py)


### Linear Quadrupole with Central Cluster ###

This is similar to the previous example but with the negative charge divided into a cluster of four -1 charges.  Notice that there is an unequal distribution of lines between the negative charges.  The number of lines is *not* proportional to the amount of charge in a 2D slice of a 3D field.  The lines are also not distributed uniformly around the negative charges.

![Linear quadrupole with central cluster.](https://raw.githubusercontent.com/tomduck/electrostatics/master/images/linear-quadrupole-cluster.png)

[Source.](https://github.com/tomduck/electrostatics/blob/master/examples/linear-quadrupole-cluster.py)


### False Monopole ###

Here we have a -4 central charge surrounded by four +1 charges.  25% of the lines diverge to infinity, which incorrectly suggests a net +1 charge.

![False monopole.](https://raw.githubusercontent.com/tomduck/electrostatics/master/images/false-monopole.png)

[Source.](https://github.com/tomduck/electrostatics/blob/master/examples/false-monopole.py)
