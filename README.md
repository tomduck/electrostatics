
electrostatics 0.1
==================

*electrostatics.py* is a python module for electrostatics field calculations and field line plots.  Install it by downloading the source and executing `python3 setup.py install` from the shell as root.  Examples that demonstrate its use are given below.

I am pleased to receive bug reports and feature requests on the project's [Issues tracker].

[Issues tracker]: https://github.com/tomduck/electrostatics/issues


Examples
--------

Standard examples are given together with a selection of cases from the excellent [paper] "Electric field lines don't work" by Wolf, Van Hook and Weeks (*Am. J. Phys., 64,* 1996).

The colours in each image give the log10 of the field magnitude.

[paper]: http://scitation.aip.org/content/aapt/journal/ajp/64/6/10.1119/1.18237


### Dipole ###

![Dipole.](https://raw.githubusercontent.com/tomduck/electrostatics/master/images/dipole.png)

[Source.](https://github.com/tomduck/electrostatics/blob/master/examples/dipole.py)


### Biased Dipole ###

The left charge is +2 and the right charge -1.  Field lines emanate symmetrically from the -1 charge, and also symmetrically in the far field.  The +2 charge exhibits "equatorial clumping" of the field lines.  The zero-field point (in black) would have lines entering from above and below in 3D so that the electric field is non-divergent.

![Biased dipole.](https://raw.githubusercontent.com/tomduck/electrostatics/master/images/biased-dipole.png)

[Source.](https://github.com/tomduck/electrostatics/blob/master/examples/biased-dipole.py)


### Biased Dipole in Flatland ###

This example is for an electric field that is non-divergent in 2D (i.e., Flatland).  Notice that the zero-field point has lines both entering and leaving it.  There is also no equatorial clumping as in the previous example.  The purported defects in the biased dipole example are an artifact of taking a slice of the 3D field.

![Biased dipole in Flatland.](https://raw.githubusercontent.com/tomduck/electrostatics/master/images/biased-dipole-flatland.png)

[Source.](https://github.com/tomduck/electrostatics/blob/master/examples/biased-dipole-flatland.py)


### Line - Point ###

Both the line and point have the same amount of charge.  Lines are distributed symmetrically around the point charge and connect to the line where they will.

![Line - point.](https://raw.githubusercontent.com/tomduck/electrostatics/master/images/line-point.png)

[Source.](https://github.com/tomduck/electrostatics/blob/master/examples/line-point.py)


### Line - Line ###

The lines are distributed equally around one line and connect to the other symmetrically.

![Line - line.](https://raw.githubusercontent.com/tomduck/electrostatics/master/images/line-line.png)

[Source.](https://github.com/tomduck/electrostatics/blob/master/examples/line-line.py)


### Cup - Point ###

![Cup - point.](https://raw.githubusercontent.com/tomduck/electrostatics/master/images/cup-point.png)

[Source.](https://github.com/tomduck/electrostatics/blob/master/examples/cup-point.py)


### Quadrupole ###

![Quadrupole.](https://raw.githubusercontent.com/tomduck/electrostatics/master/images/quadrupole.png)

[Source.](https://github.com/tomduck/electrostatics/blob/master/examples/quadrupole.py)


### Linear Quadrupole ###

The middle charge is -4 and the outer charges are +2.  Lines are distributed evenly around the positive charges.  Note the equatorial clumping around the negative charge.

![Linear quadrupole.](https://raw.githubusercontent.com/tomduck/electrostatics/master/images/linear-quadrupole.png)

[Source.](https://github.com/tomduck/electrostatics/blob/master/examples/linear-quadrupole.py)


### Linear Quadrupole with Central Cluster ###

This is like the previous example but with the negative charge divided into a cluster of four -1 charges.  Notice that there is an unequal distribution of lines between the negative charges.  The number of lines is *not* proportional to the amount of charge.

![Linear quadrupole with central cluster.](https://raw.githubusercontent.com/tomduck/electrostatics/master/images/linear-quadrupole-cluster.png)

[Source.](https://github.com/tomduck/electrostatics/blob/master/examples/linear-quadrupole-cluster.py)


### False Monopole ###

Here we have a -4 central charge surrounded by four +1 charges.  25% of the lines diverge to infinity, leading one to incorrectly surmise the net charge is +1.

![False monopole.](https://raw.githubusercontent.com/tomduck/electrostatics/master/images/false-monopole.png)

[Source.](https://github.com/tomduck/electrostatics/blob/master/examples/false-monopole.py)
