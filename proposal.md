# Proposal

## Motivation

Phase field models are a bridge between atomic-scale methods and the
macro scale and, thus, a key component of ICME workflows. However,
phase field simulations require extensive computational resources and
generate large volumes of raw field data. A FAIRer, more systematic,
approach to archiving phase field data has the potential to improve
ICME workflows substantially. Currently, researchers are hindered in
phase field research and engineering in all aspects of the FAIR
paradigm with regards to both simulation and data archiving. In
particular, developing better AI surrogate models for phase field
could be improved with a more systematic approach to simulation
management and data archiving.

In this project, we propose using a similar idea to the approach
outlined by the [Data Dictionaries Working
Group](https://www.marda-alliance.org/portfolio-item/wg-5-data-dictionaries-working-group/). They
state that "metadata that travels with the data and enrich dataset
context by making relationships to other datasets in the materials
research community explicity". In particular, this approach enables
researchers to query for datasets that are currently almost impossible
to locate and reuse without working directly with publication
authors. Currently, the [PFHub project](https://pages.nist.gov/pfhub/)
uses [its own lightweigh
ontology](https://github.com/usnistgov/pfhub-schema) to categorize and
compare phase field results for the benchmark problems published by
the CHiMaD phase field workshop participants. This takes the form of a
small YAML file with links to relevant raw or processed tabular
data. The data is archived with the YAML file alongside and the
associated link is provided to the PFHub project. We propose a similar
approach for archiving all phase field data outputs in general (not
just those from the PFHub benchmarks).

The main aim of the working group is to provide an ontology or schema
to describe phase field simulations and the corresponding data. This
might include a simple link to a problem definition, a description of
the numerical approach, computational resources used during the
simulations, categorization of the physical model as well as links and
descriptions of the data files.  As an aside, it is worth noting that
the metadata and provenance issues for storing simulation data
effectively have not been widely addressed by the materials data
community. Clearly, a successful approach to these issues within the
phase field community could be disseminated into other sub-fields of
materials science.

## Work Plan

The main aim of the working group is to generate a lightweight
ontology. However, this presents a small, but not insignificant hurdle
for the researcher publishing phase field data. A seconday aim of the
working group is to facilitate researchers in generating schema files
via templates, web forms and command line tools. The main steps in the
work plan are:

1. **Generate and finalize an initial schema**:
  - Use the [existing PFHub LinkML
    repository](https://github.com/usnistgov/pfhub-schema) as a basis
    for generating the schema.
  - Determine use cases (how would other researcher use phase field data).
  - Finalize a schema over first few months of WG

2. **Implement web tool, templates or command line to generate schema files**
  - Develop a web tool for generating schema files similar to
    [codemeta.json](https://codemeta.github.io/codemeta-generator/)
  - Create prefilled examples of the YAML / JSON files.
  - Co-opt existing or use new command line tool to query repositories, ask
    questions, populate templates and push entries to Zenodo or similar service.
  - A possible long term goal would be a phase field registry similar to PFHub.

3. **Develop working examples**
  - An example using an existing PFHub benchmark result and integrated
    into the PFHub registry.
  - An example using a study of numerical convergence using a series of
    simulations at varying discretizations.
  - An example phase field schema and associated data published in
    conjunction with a phase field publication.

4. **Approach wider phase field community for feedback**
  - Present examples and tools at CHiMaD phase field workshops
  - Present same at the MaRDA meeting
  - Present at larger conference.
  - Publicaton describing schema and case study examples.


### Goals and Expected Impact

 - Initial goal/impact would be to have the phase field schema used in conjunction with
   some phase field publications.
 - The PFHub project adopting the new schema.
 - Schema is widely used within the phase field community to publish
   results to generate FAIR content.
 - Secondary uses of the published phase field data to generate phase
   field AI surrogate models.
 - Other materials science communities adopting the standard for
   simulation data.

### Deliverables

Within 18 months of the commencement of the working group, we will
deliver:

 - A Working Group Note, published on the MaRDA Alliance website
   including some feedback from wider phase field community.
 - Implemented working examples as outlined in part 3 of the [Work
   Plan](#Work-Plan) above.
