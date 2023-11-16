# Phase Field in a Workflow

Phase Field simulations are used in a workflow in conjunction with other tools to predict the fatigue lifetime of components depending on the process parameters.
The microstructural data produced by phase field is used by an image analysis tool that extracts microstructural features, such as grain sizes, roughness, incircle and excircle radius.
These features are then used in a fatigue lifetime prediction tool.
Simulations are performed over a wide parameter range. The results and intermediate results can be used for training of AI tools that estimate the lifetime of components or optimize the process parameters for example in terms of energy or CO2 efficiency. 

## Examples
Fatigue lifetime prediction for martensitic and bainitic steels (iBain)
https://www.materialdigital.de/project/8

## Key Issues
Ideally the different tools should be decoupled, phase field produces a microstructure, and it is stored in a database, then the next tool can pick up the data. Output data should be described so that new tools that expand the workflow can easily parse the data.
Phase Field simulations can produce significant amounts of data. This might require a centralized database for simulations with decentralized data storage.

## Schema requirements for this use case
- **Description of software tools used in workflow**:
    - version (git hash, version number, local changes)
    - description of input data (data format, units, meaning)
    - description of output data (data format, units, meaning)
    - coupling to databases (e.g., Thermo-Calc)

- **Problem description**:
    - classification of simulation
    - composition
    - temperature data (e.g., cooling curve)
    
- **Results**:
    - description of results files (data format, units, meaning)

- **Intermediate Data**:
    - remote storage locations if any

- **Author**:
    - contact data

- **Experimental Data**:
    - does experimental data exist for similar process parameters
    - storage location

Meta data should be automatically provided by the workflow tool and appended as necessary by the database.
