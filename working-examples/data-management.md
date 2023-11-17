# Researcher (or group) internal comparisons & data management

Moving this to github now!

## Problem Statement

This use case represents internal use, at the same time or later on, to find simulations of similar character to compare or build on later. Given a bramble of results on disk, how to find the right dataset?

## Context

A group of researchers working together/separately on phase field and want to manage data in a coherent way to help with their own data management issues and avoid future institutional memory loss, i.e., internal FAIR protocol.
Say we have a solution from MOOSE, and want to compare the answer from PRISMS-PF. We need to know granular details of the geometry, boundaries, solver, timestepper, meshing, etc.

## Key Issues

## Schema Solutions

- [ ] **Comment** about the reason for the simulation akin to a git commit (human-readable description)
- [ ] **Specification** of the problem (a link, notebook, web page, paper, DOI, ...)
- [ ] **Dimension**
    - [ ] 0D, 1D, 2D, 3D?
    - [ ] Axisymmetric?
    - part of problem spec
- [ ] **Geometry/Domain** 
    - [ ] Regular versus irregular?
        - [ ] Regular: define $L_x \times L_y \times L_z$ and $\Delta x \times \Delta y \times \Delta z$, for example
    - [ ] Global coordinate system (Cartesian, spherical, ...); e.g., spherical shell
    - [ ] A description?
    - [ ] Link to a geometry
- [ ] ***Material***: This is somewhat defined variables and parameters of the model applied to a specific domain
    - part of problem spec
    - property values
    - text about material
    - look at other materials schema for this
- [ ] ***Physics***: Elastic energy, electric energy, etc. It is practically defined by the equations you use. However, it makes it easier to understand what the model tries to do at a glance. 
- [ ] **Equation**: `o_` (order parameter), `v_` (Thermodynamic variable), `c_` (computed property, as a function of `o_` & `v_`), `f_` (function), `d_` (derivative), `g_` (gradient), `p_` (parameters)
	- [ ] *Initial conditions*
	- [ ] *Boundary Conditions*
	- [ ] *Parameter values*
	- [ ] Part of problem spec

- [ ] **Mesh**: Based on dimensionality, this may vary. 
- [ ] **Solver**: 
	- [ ] solver parameters may vary
- [ ] *Post processing*
	- [ ] It may already be defined in a set of parameters and variables. 

