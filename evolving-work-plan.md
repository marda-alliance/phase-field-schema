# Evolving Work Plan

The main aim of the working group is to generate a lightweight
ontology. However, this presents a small, but not insignificant hurdle
for the researcher publishing phase field data. A secondary aim of the
working group is to facilitate researchers in generating schema files
via templates, web forms and command line tools. The main steps in the
work plan are:

1. **Develop use cases**

   Single page document describing a use case and possible scheme field requirements.

   Possible uses cases:
   
   - An example using an existing PFHub benchmark result and
     integrated into the PFHub registry.
   - An example using a study of numerical convergence using a series
     of simulations at varying discretizations.
   - An example phase field schema and associated data published in
     conjunction with a phase field publication.
   - An example schema use case from the perspective of archiving and then using data for
     AI training.

3. **Generate and finalize an initial schema**
   
   - Use the [existing PFHub LinkML repository][pfhub-schema] as a
     basis for generating the schema.
   - Determine use cases (how would other researcher use phase field
     data).
   - Finalize a schema over first few months of WG

4. **Implement web tool, templates or command line to generate schema
   files**
   
   - Develop a web tool for generating schema files similar to
     [codemeta.json][code-gen]
   - Create prefilled examples of the YAML / JSON files.
   - Co-opt existing or use new command line tool to query
     repositories, ask questions, populate templates and push entries
     to Zenodo or similar service.
   - A possible long term goal would be a phase field registry similar
     to PFHub.

5. **Develop working examples**

   From the use cases, develop working implementations that use the generated schema.

6. **Approach wider phase field community for feedback**:
   - Present examples and tools at CHiMaD phase field workshops
   - Present same at the MaRDA meeting
   - Present at larger conference.
   - Publication describing schema and case study examples.

<!-- links -->
[code-gen]: https://codemeta.github.io/codemeta-generator/
[pfhub-schema]: https://github.com/usnistgov/pfhub-schema
