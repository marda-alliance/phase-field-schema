# Comparing the Performance of Solver Approaches Use Case

## Problem statement

How can we compare the results of phase-field codes to gain insight into which
numerical/computational approaches are best suited to a given problem?

## Context

A wide variety of numerical solution approaches are used for phase-field
simulations. Even for a single code (e.g. MOOSE), many solver settings are
available, and these can have a substantial impact on the accuracy and
computational performance. Combined with databases with performance (and error)
data, improved ability to determine which approaches were used in which
simulations may provide insight into which combination of approaches are best
suited to certain phase-field application areas. Automated metadata generation
by code developers could provide the necessary information for users to archive
with their results.

## Examples of such activities in the literature

DeWitt, S., Rudraraju, S., Montiel, D. _et al._
PRISMS-PF: A general framework for phase-field modeling with a matrix-free
finite element method. _npj Comput Mater_ **6** (2020) 29.
DOI: [10.1038/s41524-020-0298-5](https://doi.org/10.1038/s41524-020-0298-5).

This paper contains a comparison of the accuracy and computational cost for
several open-source phase-field modeling codes for PFHub Benchmark 3 (dendritic
solidification of a pure material). The results were manually pulled from PFHub
uploads, with some information needing to be manually extracted from input
files from different codes.

## Key issues

1. Any given phase-field simulation employs a hierarchy of numerical
   approaches, with variants that are not straightforward to classify.
   Often key details about methods are left out of publications.
2. In some cases, users may not know all of the implementation details of the
   code they use. (In part by design -- a goal of open-source community codes
   is that not everyone needs to get into the weeds of the implementation.)

## How would a community schema help?

It would clarify which numerical and computational approaches were used to
generate a particular result.

## Schema requirements for this use case

- A hierarchical description of numerical methods and approaches

  - Temporal discretization
    - Scheme name
    - Type (Implicit, Explicit, Semi-implicit)
    - Expected order of accuracy
    - Adaptivity (Adaptive, Fixed)
      - Adaptivity scheme name

  - Spatial discretization
    - Type (FD, FE, FV, pseudospectral)
    - Expected order of accuracy
    - Mesh type (structured, unstructured, hex/tet)
    - Adaptivity (Adaptive, Fixed)
      - Adaptivity scheme name

  - Linear solver
    - Scheme name
    - Type (Iterative, Direct)
    - Preconditioner

  - Nonlinear solver
    - Scheme name

  - Parallelism
    - Distributed-memory parallelism approach
    - Shared-memory parallelism approach
      - Targeted hardware (CPU, GPU)
      - Libraries or standards (OpenMP, CUDA, Kokkos, HIP, Threads)

- Buy-in from software developers to auto-generate the relevant metadata
