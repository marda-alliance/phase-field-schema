# Automated RO-Crate Provenance for FiPy Phase-Field Benchmarks

This repository contains the numerical execution and automated metadata capture
workflow for PFHub Benchmark 8a (Homogeneous Nucleation). It demonstrates the
generation of a FAIR-compliant Workflow Run RO-Crate (WRROC) directly from the
FiPy simulation runtime.

## Architecture

The project utilizes a unified, highly reproducible environment powered by Nix
(`flake-parts`) and `uv2nix`. This single-closure architecture binds the C++
multiphysics stack (FiPy/SciPy) together with the semantic metadata
serialization tools (`rocrate`, `frictionless`).

## Environment Setup & Execution

To bootstrap the environment and run the benchmark:

1. **Generate the Lockfile**
   Ensure the `uv.lock` file is synced with `pyproject.toml`. If you do not have `uv` installed globally, run it via `nixpkgs`:
   ```bash
   nix run nixpkgs#uv -- lock
   ```
   
2. Enter the Unified Environment
   Drop into the reproducible shell containing all simulation and metadata dependencies:
   ```bash
   nix develop
   ```

3. Execute the Simulation
   Run the benchmark script. The outputs will populate the data/ directory:
   ```bash
   python benchmark8a.py params8a.yaml
   ```

## Published

An example RO-Crate is published at https://zenodo.org/records/20647927
