# General Notes and Ideas for the WG

## Motivation

Long version of the motivation

### Why do we need structured phase field data?

Phase field models are characterized by a particular form of PDE
related to an Eulerian free boundary problem and defined by a diffuse
interface. Phase field models for practical real world applications
require sufficient high fidelity to resolve both the macro length
scale related to the application and the micro length scales
associated with the free boundary. This requires extensive
computationally resources and generates large volumes of raw field
data. This data consists of field variables defined frequently across
a domain or interpolation function with many Gauss points each defined
at multiple time steps. In recent years there have been efforts to use
AI to address the computational expense associated with phase field
simulations via surrogate models or more direct approaches. However,
for AI practitioners to leverage relevant phase field resources a more
systematic approach is required for archiving and accessing
data. Furthermore, it is often difficult for phase field practitioners
to find and access raw or minimally processed data from phase field
simulations, before the post-processing step and final publication. In
the following sections we will discuss how we can motivate phase field
practitioners to publish their data and assuming that barrier is
crossed, how to make it straightforward to include sufficient metadata
for the raw and minimally processed data to be actually useful for
others.

Let's consider a researcher constructing a robust transfer learning
surrogate model for the Cahn-Hilliard problem.  The researcher might
require raw data from a variety of different numerical schemes,
parameter ranges, grid resolutions, different domains all of which
will be used to assess the robustness and accuracy of the transfer
model. Generating all the data from this wide variety of parameters
and initial condition would be prohibitively expensive, not to mention
impractical from a research and knowledge standpoint. However,
leveraging the vast volume of previous Cahn-Hilliard simulations would
be possible if that data was both findable and accessible, which is
not the case currently. This working group aims to address the issues
of finding and accessing phase field data and leave the more complex
problem of interoperability and reproduciblity for subsequent work.

As an aside, it is worth noting that the schema / metatdata /
provenance / ontology issues of storing simulation data effectively
have not been widely addressed by the materials data
community. Clearly, a successful approach to these issues within the
phase field community could be disseminated into other sub-fields of
materials science.

### How would a lightweight ontology help?

In this project, we propose using a similar idea to the approach
outlined by the [Data Dictionaries Working
Group](https://www.marda-alliance.org/portfolio-item/wg-5-data-dictionaries-working-group/). They
state that "metadata that travels with the data and enrich dataset
context by making relationships to other datasets in the materials
research community explicity". In particular, as described in the
previous sections, this approach enables researchers to query for
datasets that are currently hard to find.

The PFHub project uses [its own lightweigh
ontolgoy](https://github.com/usnistgov/pfhub-schema) to categorize and
compare phase field results for the benchmark problems published by
the CHiMaD phase field workshop participants. This takes the form of a
small YAML file with links to relevant raw or processed tabular
data. The data is archived with the YAML file alongside and then this
link is provided to the PFHub project. The PFHub project is in fact a
regirstry of these links and the website can then query the data from
these links and make comparison plots based on the contents of the
YAML files. This approach is agnostic to the data archive or
infrastrcuture used for storing the data. The YAML file has to provide
enough metadata that the PFHub project can access the raw data and
provide useful data comparisons on the website.

The ontology / schema will be developed by the working group, but some
simple areas to address might include a link to a problem definition,
a simple description of the numerical approach, computational
resources, categorization of the physical model as well as links and
descriptions of the data files.

### What would the motivation for the community to adopt the lightweight ontology?

The lightweight ontology approach, assuming the researcher is
motivated to publish raw data, is only a minimal barrier to the
process of data archiving.  The main hurdle for the researcher is
generating the YAML file. The working group would aim to provide
resources via templates, web form and command line tools to help with
this process.

The long term aim of the developed schema would be to assist in
generating a registry of phase field simulations similar to PFHub, but
much expanded to include a wide variety of problem specifications and
results. This approach might motivate researchers to be more engaged
in publising raw data and provide the necessary metadata if they know
that there efforts will results in immediate feedback and engagement.

## List of plannning, goals, impacts, deliverables

This has no particular order

 - Finalize an initial schema and format similar to the existing PFHub schema, but more complete
 - Generate web tool, templates and command line tool to generate metadata ontology files
 - Generate archived examples on a variety of data archive sites using PFHub benchmarks
 - Generate compelling data aggregation data view case study from the above examples to demonstrate the advantages of the proposed approach
 - Approach the wider phase field community to garner interest and provide feedback

 - A schema generated by LinkML or similar tool in variety of file formats
 - Case study and tools as outlined above
 - Report from the wider phase field community
 - A Working Group Note, published on the MaRDA Alliance website including some feedback from wider phase field community
 - Implemented examples of usage and data aggregation as outlined above.
