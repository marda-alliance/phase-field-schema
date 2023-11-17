# Researcher (or group) internal comparisons & data management

## Problem Statement

How could a research group coordinate and pracitce FAIR principles
using a community schema standard?

## Context

A materials research group with multiple members participating in
projects might have some members running phase field simulations and
some working on other aspects of materials design, but collaborating
with the phase field practitioners in some way. In this scenario, it is
important for the group to have a plan to archive each individual or
series of phase field simulation in a coherent way to improve research
coordination. Furthermore, having an effective archive of past
simulations allows future member of the group to have a better groups
of previous work and improves institutional memory.


# Key Issues

An important aspect of this is finding previous simulations based on
aspects of the problem specification. This is a major difference from
other use cases. The problem specification becomes more important as
the problem specification is unlikely to be written up or published in
an archived location. Also, a reseach group will have vast bramble of
archived simuatlions on disk so searching the schema for meaningful
results (e.g. results of a similar character based on parameter values
or dervied quantity) becomes important.

## Schema Solutions

- **Comment**: 
  - Reason for the simulation akin to a git commit (human-readable
    description)
- **Specification** 
  - Link to document (notebook, web page, paper, DOI, ...)
  - Dimension (0D, 1D, 2D, 3D, axisymmetric?)
  - Geometry / Domain
    - Application
    - Regular versus irregular?
        - Regular: define $L_x \times L_y \times L_z$ and $\Delta x
          \times \Delta y \times \Delta z$, for example
        - Axisymmetric
    - Global coordinate system (Cartesian, spherical, ...); e.g.,
      spherical shell
    - A description?
    - Link to a geometry schema file or STL
    - Material: This is somewhat defined variables and parameters of
      the model applied to a specific domain
      - part of problem spec
      - property values
      - text about material
      - look at other materials schema for this
    - Physics:
      - Elastic energy, electric energy, etc. It is practically
        defined by the equations you use. However, it makes it easier
        to understand what the model tries to do at a glance.
      - *Initial conditions*
      - *Boundary Conditions*
      - *Parameter values*
- **Mesh**:
  - Based on dimensionality, this may vary. 
- **Solver**: 
  -  solver parameters may vary
- **Post processing**
  - It may already be defined in a set of parameters and variables. 

