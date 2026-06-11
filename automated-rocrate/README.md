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

## TODO

# Development Roadmap: WRROC Integration

## Phase 1: Environment Architecture (Completed)

- [x] Consolidate dual Nix flakes into a single `flake-parts` architecture.
- [x] Migrate dependency resolution from `poetry2nix` to `uv2nix`.
- [x] Fix `hatchling` build errors by setting `[tool.uv] package = false` for a non-packaged workspace.
- [x] Verify simulation execution (`benchmark8a.py`) within the unified shell.

## Phase 2: Refactoring Metadata Extraction (Next)

- [ ] **Draft `fipy_rocrate.py`:** Convert the disconnected `cli.py` logic into a stateful `WROCManager` class.
  - Implement initialization logic to capture prospective config (`params8a.yaml`) and system state.
  - Implement finalization logic to capture retrospective metrics (wall time, memory utilization, dynamic VTK/HDF5 output paths).
- [ ] **Instrument `benchmark8a.py`:**
  - Inject `WROCManager.start()` immediately after configuration parsing.
  - Inject `WROCManager.finalize()` at the termination of the solver time loop.
- [ ] **Validate JSON-LD Output:** Ensure `ro-crate-metadata.json` conforms strictly to the WRROC Process Run profile.

## Phase 3: Manuscript Integration (Pending)

- [ ] **Update Section 3.3 (LaTeX):** Document this in-situ Python metadata extraction methodology.
- [ ] Rewrite the methodology text to emphasize the elimination of manual configuration files in favor of native runtime hooks.
- [ ] Ensure the LaTeX `\dirtree` figure perfectly matches the final file structure.
