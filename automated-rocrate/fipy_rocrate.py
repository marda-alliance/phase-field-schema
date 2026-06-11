import datetime
import time
import tomllib
import yaml
from pathlib import Path

from rocrate.rocrate import ROCrate
from rocrate.model.softwareapplication import SoftwareApplication
from rocrate.model.person import Person
from rocrate.model.entity import Entity
from rocrate.model.contextentity import ContextEntity

class WROCManager:
    """
    Stateful lifecycle manager for automated Workflow Run RO-Crate (WRROC) generation.
    Handles prospective metadata parsing and retrospective runtime harvesting.
    """
    def __init__(self, run_name: str, run_description: str, input_yaml: str, script_path: str):
        self.input_yaml = Path(input_yaml)
        self.script_path = Path(script_path)
        self.start_time = None

        self.crate = ROCrate()

        # 1. Base Crate Configuration
        self.crate.name = run_name
        self.crate.description = run_description
        self.crate.root_dataset["conformsTo"] = {"@id": "https://w3id.org/ro/wfrun/process/0.4"}

        # 2. Parse Project TOML for Authorship and License
        with open("pyproject.toml", "rb") as f:
            pyproject = tomllib.load(f)

        ro_config = pyproject.get("tool", {}).get("rocrate", {})

        # Register Authors
        author_entities = []
        for key, data in ro_config.get("authors", {}).items():
            author = self.crate.add(
                Person(
                    self.crate,
                    identifier=data.get("orcid", f"#{key}"),
                    properties={
                        "name": data["name"],
                        "affiliation": data.get("affiliation", "")
                    }
                )
            )
            author_entities.append(author)
        self.crate.root_dataset["author"] = author_entities

        # Register License
        lic_data = ro_config.get("license", {})
        if lic_data:
            self.crate.root_dataset["license"] = self.crate.add(
                Entity(
                    self.crate,
                    identifier=lic_data.get("identifier", "#license"),
                    properties={"@type": "CreativeWork", "name": lic_data.get("name", "License")}
                )
            )

        script_file = self.crate.add_file(self.script_path, dest_path=self.script_path.name)

        # 3. Register Instrument (The Execution Script)
        self.instrument = self.crate.add(
            SoftwareApplication(
                self.crate,
                identifier=self.script_path.name,
                properties={
                    "name": self.script_path.name,
                    "programmingLanguage": "Python"
                }
            )
        )

        # 4. Parse YAML inputs to PropertyValues
        with open(self.input_yaml, "r") as f:
            self.params = yaml.safe_load(f)

        param_entities = []
        for k, v in self.params.items():
            if v is not None:
                param_entities.append(
                    self.crate.add(
                        ContextEntity(
                            self.crate,
                            identifier=f"#param-{k}",
                            properties={
                                "@type": "PropertyValue",
                                "name": k,
                                "value": str(v)
                            }
                        )
                    )
                )

        self.input_file = self.crate.add_file(
            self.input_yaml,
            dest_path=self.input_yaml.name,
            properties={
                "name": "Simulation Parameters",
                "encodingFormat": "text/yaml",
                "variableMeasured": param_entities
            }
        )

        # 5. Capture Reproducibility Environment Files
        for env_file in ["pyproject.toml", "uv.lock", "flake.nix"]:
            path = Path(env_file)
            if path.exists():
                encoding = "application/toml" if env_file == "pyproject.toml" else "text/plain"
                self.crate.add_file(
                    source=path,
                    dest_path=path.name,
                    properties={
                        "name": f"Environment specification: {env_file}",
                        "encodingFormat": encoding
                    }
                )

        # 6. Link and Download the PFHub Benchmark Specification
        benchmark_url = "https://github.com/usnistgov/pfhub/raw/master/benchmarks/benchmark8.ipynb"
        canonical_id = "https://pages.nist.gov/pfhub/benchmarks/benchmark8.ipynb/"

        try:
            # fetch_remote=True downloads the file into the crate directory for offline use
            bench_file = self.crate.add_file(
                source=benchmark_url,
                fetch_remote=True,
                properties={
                    "@id": canonical_id,
                    "name": "PFHub Benchmark 8: Homogeneous Nucleation",
                    "encodingFormat": "application/x-ipynb+json",
                    "url": benchmark_url
                }
            )
            # Semantically declare that this entire simulation is based on this benchmark
            self.crate.root_dataset["isBasedOn"] = bench_file
        except Exception as e:
            print(f"Warning: Could not fetch remote benchmark notebook: {e}")
            # Fallback to just adding a semantic link if the system is offline (e.g., HPC node)
            bench_entity = self.crate.add(
                Entity(
                    self.crate,
                    identifier=canonical_id,
                    properties={
                        "@type": ["CreativeWork", "SoftwareSourceCode"],
                        "name": "PFHub Benchmark 8: Homogeneous Nucleation",
                        "url": benchmark_url
                    }
                )
            )
            self.crate.root_dataset["isBasedOn"] = bench_entity

    def start(self):
        """Invoke at simulation loop init to freeze start time."""
        self.start_time = datetime.datetime.now(datetime.timezone.utc)
        self.start_perf = time.perf_counter()

    def _parse_tabular_header(self, filepath: Path) -> list:
        """Reads the first non-comment line of a tabular file to infer columns."""
        cols = []
        try:
            with open(filepath, "r") as f:
                for line in f:
                    if not line.strip() or line.startswith("#"):
                        continue
                    # FiPy saves using \t by default
                    headers = [h.strip() for h in line.split("\t")]
                    for h in headers:
                        if h:
                            cols.append(
                                self.crate.add(
                                    ContextEntity(
                                        self.crate,
                                        identifier=f"{filepath.name}#col-{h}",
                                        properties={
                                            "@type": "PropertyValue",
                                            "name": h
                                        }
                                    )
                                )
                            )
                    break
        except Exception as e:
            print(f"Warning: Failed to parse header from {filepath}: {e}")
        return cols

    def finalize(self, output_paths: list[str]):
        """Invoke at termination to record retrospective data and compile the JSON-LD graph."""
        end_time = datetime.datetime.now(datetime.timezone.utc)
        wall_time = time.perf_counter() - self.start_perf

        run_id = f"#run-{int(time.time())}"
        create_action = self.crate.add(
            ContextEntity(
                self.crate,
                identifier=run_id,
                properties={
                    "@type": "CreateAction",
                    "name": "FiPy Simulation Execution",
                    "startTime": self.start_time.isoformat(),
                    "endTime": end_time.isoformat(),
                    "actionStatus": "CompletedActionStatus",
                    "instrument": self.instrument,
                    "object": [self.input_file]
                }
            )
        )

        # Log Wall Time
        create_action["resourceUsage"] = [
            self.crate.add(
                ContextEntity(
                    self.crate,
                    identifier=f"{run_id}-walltime",
                    properties={
                        "@type": "PropertyValue",
                        "name": "Wall Time",
                        "value": f"{wall_time:.4f}",
                        "unitCode": "SEC"
                    }
                )
            )
        ]

        # Process Outputs Dynamically
        results = []
        for path_str in output_paths:
            p = Path(path_str)
            if p.is_dir():
                targets = p.rglob("*")
            else:
                targets = [p]

            for target in targets:
                if not target.is_file():
                    continue

                file_props = {"name": target.name}

                # Auto-inference based on file type
                if target.suffix == ".txt":
                    file_props["encodingFormat"] = "text/plain"
                    file_props["description"] = "Tabular simulation statistics"
                    file_props["variableMeasured"] = self._parse_tabular_header(target)
                elif "".join(target.suffixes) == ".tar.gz":
                    file_props["encodingFormat"] = "application/gzip"
                    file_props["description"] = "Transient phase-field mesh data"

                results.append(self.crate.add_file(
                    source=target,
                    dest_path=target,
                    properties=file_props
                ))

        create_action["result"] = results
        self.crate.root_dataset["mentions"] = [create_action]

        crate_dir = Path("crate")
        crate_dir.mkdir(exist_ok=True)
        self.crate.write(crate_dir)
