## FiPy Example

This example runs a short FiPy simulation to generate data for
demonstration purposes.

## Installation

In a clean Python environment install FiPy.

    $ poetry install .
	
in the `fipy/` directory. 

## Usage

Run the simulation with 

    $ python benchmark8.py params8a.yaml

This will generate a `data/` directory.

## RO-Crate

To generate the RO-Crate install rocrate-cli (see `../README.md`) and run

    $ rocrate-cli generate config.yaml
	
This will generate a `crate/` directory with the
`ro-crate-metadata.json` file and associated data.
