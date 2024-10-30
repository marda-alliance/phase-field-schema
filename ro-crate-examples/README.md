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

Currently there are two examples to run. The `simple` example can be
run with,

    $ rocrate_cli generate simple/config.yaml --dest simple/crate
	
which will generate a `crate/` directory along with the
`ro-crate-metadata.json` file and associated data. The `fipy` crate
can be generated in a similar manner, however, it requires the data to
be generated first. To generate the data follow the instructions in
`fipy/README.md`.
