{
  description = "Unified FiPy Simulation and WRROC Generation Environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-parts.url = "github:hercules-ci/flake-parts";

    # Python environment management via uv
    pyproject-nix = {
      url = "github:pyproject-nix/pyproject.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    uv2nix = {
      url = "github:pyproject-nix/uv2nix";
      inputs.pyproject-nix.follows = "pyproject-nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    pyproject-build-systems = {
      url = "github:pyproject-nix/build-system-pkgs";
      inputs.pyproject-nix.follows = "pyproject-nix";
      inputs.uv2nix.follows = "uv2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = inputs@{ flake-parts, nixpkgs, uv2nix, pyproject-nix, pyproject-build-systems, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      systems = [ "x86_64-linux" "aarch64-linux" "aarch64-darwin" "x86_64-darwin" ];

      perSystem = { pkgs, system, ... }:
        let
          # 1. Parse the local workspace
          workspace = uv2nix.lib.workspace.loadWorkspace { workspaceRoot = ./.; };

          # 2. Generate an overlay bridging uv.lock definitions with nixpkgs
          overlay = workspace.mkPyprojectOverlay {
            sourcePreference = "wheel";
          };

          # 3. Apply the overlay to the standard Python 3.11 package set
          python = pkgs.python311;

          # FIX: Changed `paths` to `packages` and `extend` to `overrideScope`
          pythonSet = (pkgs.callPackage pyproject-nix.build.packages {
            inherit python;
          }).overrideScope (
            pkgs.lib.composeManyExtensions [
              pyproject-build-systems.overlays.default
              overlay

              # Custom build overrides for scientific/metadata packages if wheels fail
              (final: prev: {
                petl = prev.petl.overrideAttrs (old: {
                  nativeBuildInputs = (old.nativeBuildInputs or []) ++ [ final.setuptools ];
                });
              })
            ]
          );

          # 4. Construct the virtual environment derivation
          venv = pythonSet.mkVirtualEnv "fipy-wroc-env" workspace.deps.default;
        in
        {
          devShells.default = pkgs.mkShell {
            buildInputs = [
              venv
              pkgs.uv
            ];

            shellHook = ''
              export PYTHONPATH=$PWD
              echo "Loaded unified FiPy + WRROC uv2nix environment."
            '';
          };
        };
    };
}
