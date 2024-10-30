## RO-Crate Examples

This directory is under construction, but the goal is to create a
simple CLI for generating RO-Crate given a config file and associated
data. The `rocrate_cli` directory includes the Python code for the CLI
tool. Other directories provide example config files and data.

## Installation

The command line tool can be installed using 

    $ pip install .

from the `ro-crate-examples` directory.

## Usage

Currently there is only one example to test in the `fipy`
directory. Firstly read `fipy/README.md` to generate the require
data and then use

    $ rocrate_cli generate fipy/config.yaml
	
to generate a `crate/` directory with the `ro-crate-metadata.json`
file and associated data.
