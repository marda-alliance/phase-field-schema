# PFHub Use Case

## Problem Statement

Can a community phase field schema support data ingestion for the
phase field benchmarking project?

## Context

In essence, at the core of the PFHub project is a registry of phase
field results for each phase field benchmark specification. The goal
of the registry is to provide quality assurance to phase field codes
by providing adequate accuracy and uncertainty quantification for
submitted benchmark results. The current iteration of PFHub requires
submissions to provide a metadata file alongside the required
post-processed data. This metadata file facilitates the digestion of
data specifications unique to each benchmark problem. The uploaded
data is presented in comparison plots aggregated across submissions
for each benchmark problem. The PFHub approach can be thought of in
the context of the model-view-controller (MVC) paradigm. The metadata
file behaves as the model (or schema) where all the fields required by
PFHub must be defined. The controller is a Python utility that can
read the model and, thus, the data and then aggregate the data into
dataframes for the view. The view takes those dataframes and displays
the aggregated data in Jupyter notebooks. The MVC paradigm depends
crucially on how the model is defined and the inability to specify a
more complete model has hindered the PFHub project in a number of
ways.

## Key Issues

Overall PFHub has made progress in sharing and compiling the results
to the benchmark problems. However, there are a number of issues with
the current system for data submission. These problems can be
enumerated as follows:

1. The benchmarks currently have no gold standard solutions for
   comparison with the submitted results and, thus, it is difficult to
   validate submissions.
2. The current metadata scheme lacks many relevant fields inhibiting a
   broader range of queries and data views.
3. The benchmark specifications as written require pinning data
   formats, file names and columns descriptions prohibiting
   flexibility and convenience in data management choices.
4. The benchmark specifications require users to post-process results
   into tabular data formats. Submission of raw field data from phase
   field simulations might provide more sophisticated benchmark
   comparisons and automated post-processed data views (e.g. automated
   order of accuracy or uncertainty metrics).

## How would a community schema help?

1. A community schema would not directly address the issue of gold
   standard solutions.
2. A systematic linked data approach for recording both the
   prospective and retrospective metadata for simulation execution as
   well as the software framework metadata would greatly improve the
   options for querying submission results.
3. An agreed upon set of raw and post-processed data categories,
   naming conventions and formats will reduced the complexity of PFHub
   submissions. Furthermore, data sharing can become more automated
   with a systematic approach to data descriptors.
4. Improving data conventions would help PFHub users more readily
   share field data by making the storage and description of field
   data more standardized.

## Solution and Recommendation

The following are specific details for the community schema that would
address the above issues. A useful publication to help with this is
[*Sharing interoperable workflow provenance*][SHARING]. It identifies
5 broad categories of data (the problem specification is included as a
separate category here).

- **Problem specification**: a link to the benchmark specification in
  the case of PFHub. For other applications this may need to be more
  complete.
- **Retrospective provenance metadata**: descriptions of metadata that
  can only be gathered during or after a simulation event.
- **Prospective provenance metadata**: large amount of metadata known
  before the simulation.
- **Data sharing**: a description of post-processed and raw data for
  each problem specification in the case of the benchmarks.
- **Environment execution**: possible inclusion of an execution
  container, software description and input files
- **Findability**: links to relevant repositories and DOI of shared
  data

The following bullets outline specific fields that might be included
in a prospective schema.

- **Problem specification**:
  - DOI link to a problem specification
  - Keywords related to the phase field application and typically used
    for materials ontologies (e.g. "additive-manufacturing" or
    "cobalt-alloy")
  - A phase field equation category (e.g. "cahn-hilliard" or
    "allen-cahn")
- **Retrospective provenance metadata**:
  - Memory usage, run time
  - mesh actually used, degrees of freedom
- **Prospective provenance metadata**:
  - Computer architectures, nodes, threads etc
  - Control parameter settings, command line options, environment
    variables
  - Numerical approach
    - meshing strategy, nominal degrees of freedom
    - non-linear solver strategy
    - linear solver strategy
    - time-stepping strategy
    - discretization strategy
      - expected order of accuracy
- **Data Sharing**:
  - Suggested naming conventions, formats for
    - time
    - phase field global quantities
    - field data
  - Suggested storage formats
  - URL or local paths to data files
  - DOI of data files
  - Domain / mesh file details if relevant for reading data
  - Formatting details
- **Environment Execution**:
  - Link to software framework
    ([Codemeta][CODEMETA]) + repository +
    version
  - Facilitate execution
    - Link to container image
    - Link to environment generation files
      (e.g. `environment.yml`, `shell.nix` or `Dockerfile`)
  - Link to relevant input files + commit ID
  - implementation repository link  + commit ID
- **Findability**:
  - Implementation repository link + commit ID
  - DOI of implementation repository
  - DOI of output files

[SHARING]: https://doi.org/10.1093/gigascience/giz095
[CODEMETA]: https://codemeta.github.io/terms/
