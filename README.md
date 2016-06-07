
electrostatics 0.1
==================

*electrostatics.py* is a python module for electrostatics field calculations and field line plots.  Install it by downloading the source and executing `python3 setup.py install` from the shell as root.  Examples that demonstrate its use are given below.

I am pleased to receive bug reports and feature requests on the project's [Issues tracker].

[Issues tracker]: https://github.com/tomduck/electrostatics/issues


Examples
--------

Textbook examples are provide along with a selection of cases from the excellent [paper] "Electric field lines don't work" by Wolf, Van Hook and Weeks (*Am. J. Phys., 64,* 1996).

In each case lines are initialized symmetrically close to one (or more) charges.  Paths are determined numerically from the [streamline equation] using the `vode` ODE solver.

The colours in each image give the logarithm (base-10) of the field magnitude.

[paper]: http://scitation.aip.org/content/aapt/journal/ajp/64/6/10.1119/1.18237

[streamline equation]: http://folk.uib.no/fcihh/seminar/lec1.pdf


### Dipole ###

The left charge is +1 and the right charge is -1.  In "textbook examples" like this the lines are symmetrically distributed around each charge no matter which charge they are initialized around.

![Dipole.](https://raw.githubusercontent.com/tomduck/electrostatics/master/images/dipole.png)

[Source.](https://github.com/tomduck/electrostatics/blob/master/examples/dipole.py)


### Biased Dipole ###

The left charge is +2 and the right charge -1.  Field lines are initialized symmetrically around the -1 charge, and again symmetrically in the far field.  Notice that the +2 charge exhibits "equatorial clumping" of the field lines.  This is the expected behaviour (see [Wolf et al, 1996][paper]).  Notice that the zero-field point (in black) has two lines exiting it.  There are lines entering from above and below in 3D so that the electric field is non-divergent.  Clumping and 2D divergence are artefacts of taking a 2D slice of a 3D field.

![Biased dipole.](https://raw.githubusercontent.com/tomduck/electrostatics/master/images/biased-dipole.png)

[Source.](https://github.com/tomduck/electrostatics/blob/master/examples/biased-dipole.py)


### Biased Dipole in Flatland ###

This example is for a theoretical electric field that is non-divergent in 2D (i.e., [Flatland]).  There is no clumping and the zero-field point has the same number of lines entering and leaving it, as expected.  This example confirms that the calculations are correct.

[Flatland]: https://en.wikipedia.org/wiki/Flatland

![Biased dipole in Flatland.](https://raw.githubusercontent.com/tomduck/electrostatics/master/images/biased-dipole-flatland.png)

[Source.](https://github.com/tomduck/electrostatics/blob/master/examples/biased-dipole-flatland.py)


### Line - Point ###

Both the line and point have the same amount of charge.  Lines are initialized symmetrically around the point charge.  That they are not symmetric where they connect to the line is a 2D slice artefact.

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

Another "textbook example" with perfect symmetry.

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

Here we have a -4 central charge surrounded by four +1 charges.  25% of the lines diverge to infinity, leading a distant observer to incorrectly surmise a net +1 charge.

![False monopole.](https://raw.githubusercontent.com/tomduck/electrostatics/master/images/false-monopole.png)

[Source.](https://github.com/tomduck/electrostatics/blob/master/examples/false-monopole.py)
