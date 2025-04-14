"""Main functions for RO-Crate CLI for phase field simulations
"""

import os
import urllib

from rocrate.rocrate import ROCrate
from rocrate.model.person import Person
from rocrate.model.entity import Entity
import yaml
from toolz.curried import curry, pipe
from toolz.curried import map as fmap
import click

from . import test as rocrate_cli_test

EPILOG = "See the documentation in the README"


@click.group(epilog=EPILOG)
def rocrate_cli():
    """Generate an ro-crate from a phase field example"""


@rocrate_cli.command(epilog=EPILOG)
@click.argument(
    "config",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    default="./ro-crate-config.yaml",
)
@click.option(
    "--dest",
    "-d",
    help="destination directory",
    default="./crate",
    type=click.Path(exists=False, writable=True, file_okay=False),
)
def generate(config, dest):
    """Generate an RO-Crate example

    Args:
      path: path to the config yaml file
      dest: destination directory
    """
    if os.path.exists(dest):
        raise click.UsageError(f"The {dest} directory already exists")
    data = read_yaml(config)
    generate_(data, dest, os.path.dirname(config))


def read_yaml(filepath):
    """Read a yaml file"""
    with open(filepath, "r", encoding="utf-8") as file:
        yaml_content = yaml.safe_load(file)
    return yaml_content


@curry
def set_attr(obj, key, value):
    """Set an attribute of an object"""
    setattr(obj, key, value)
    return obj


@curry
def add_authors(authors, crate):
    """Add the authors to a crate"""
    return pipe(
        authors,
        fmap(
            lambda x: crate.add(
                Person(
                    crate,
                    x["orcid"],
                    properties={"name": x["name"], "affiliation": x["affiliation"]},
                )
            )
        ),
        list,
        set_root("author", crate=crate),
    )


@curry
def add_license(license_, crate):
    """Add the license to a crate"""
    return pipe(
        license_,
        lambda x: crate.add(
            Entity(
                crate,
                identifier=license_["identifier"],
                properties={
                    "@type": "CreativeWork",
                    "name": license_["name"],
                    "description": license_["description"],
                    "url": license_["url"],
                },
            )
        ),
        set_attr(crate, "license"),
    )


def isabs(path):
    """Check if a path is an absolute or relative path"""
    return (
        urllib.parse.urlparse(str(path)).scheme in ("http", "https", "file")
    ) or os.path.isabs(path)


def makeabs(basepath, filename):
    """Make a file name an absolute path"""
    if isabs(filename):
        return filename
    return os.path.join(basepath, filename)


@curry
def add_files(files, crate, basepath):
    """Add a series of files to the crate"""
    return list(
        fmap(
            lambda x: crate.add_file(
                makeabs(basepath, x["path"]),
                fetch_remote=x["download"],
                properties={
                    "name": x["name"],
                    "encodingFormat": x["encodingFormat"],
                    "description": x["description"],
                    "variableMeasured": add_columns(
                        x.get("columns", []), x["path"], crate
                    ),
                },
            ),
            files,
        )
    )


@curry
def add_column(path, crate, column):
    """Add a column for table data as a PropertyValue"""
    identifier = path + "#" + column["identifier"]
    crate.add_jsonld(
        {
            "@id": identifier,
            "@type": "PropertyValue",
            "unitCode": column.get("unit", None),
            "name": column.get("name", column.get("identifier", None)),
            "description": column["description"],
            "value": column.get("value", None),
        }
    )
    return {"@id": identifier}


@curry
def add_columns(columns, path, crate):
    """Add multiple column enitites as PropertyValues"""
    return list(fmap(add_column(path, crate), columns))


@curry
def add_tabular_file(file, basepath, crate):
    """Add tabular data to a crate"""
    if file["type"] == "directory":
        return crate.add_directory(
            makeabs(basepath, file["path"]),
            properties={
                "description": file["description"],
                "encodingFormat": file["encodingFormat"],
                "name": file["name"],
                "variableMeasured": add_columns(
                    file.get("columns", []), file["path"], crate
                ),
            },
        )
    return crate.add_file(
        makeabs(basepath, file.get("path", "./")),
        fetch_remote=file.get("download", False),
        properties={
            "@type": ["File", "Dataset"],
            "description": file["description"],
            "encodingFormat": file.get("encodingFormat", None),
            "name": file["name"],
            "url": file.get("url", None),
            "keywords": file.get("keywords", None),
            "variableMeasured": add_columns(
                file.get("columns", []), file["path"], crate
            ),
        },
    )


@curry
def add_tabular_files(files, basepath, crate):
    """Add files that are tabular data to a crate"""
    return list(fmap(add_tabular_file(basepath=basepath, crate=crate), files))


@curry
def set_root(key, value, crate):
    """Set a root value"""
    crate.root_dataset[key] = value
    return crate


@curry
def add_dependency(crate, dependency):
    """Add a software dependency"""
    return crate.add(
        Entity(
            crate,
            identifier=dependency["identifier"],
            properties={
                "@type": "SoftwareApplication",
                "description": dependency["description"],
                "name": dependency["name"],
                "url": dependency["url"],
                "version": dependency["version"],
            },
        )
    )


@curry
def add_implementation(implementation, dependencies, crate):
    """Add the implementation section"""
    implementation_ = crate.add(
        Entity(
            crate,
            identifier=implementation["identifier"],
            properties={
                "@type": "SoftwareApplication",
                "conformsTo": "https://bioschemas.org/profiles/ComputationalTool/1.0-RELEASE",  # noqa: E501 # pylint: disable=line-too-long
                "description": implementation["description"],
                "name": implementation["name"],
                "applicationCategory": implementation["applicationCategory"],
                "url": implementation["codeRepository"],
                "codeRepository": implementation["codeRepository"],
                "programmingLanguage": implementation["programmingLanguage"],
            },
        )
    )

    implementation_["softwareRequirements"] = list(
        fmap(add_dependency(crate), dependencies)
    )

    return implementation_


@curry
def add_workflow(data, basepath, crate):
    """Add the workflow entity to the crate"""
    workflow = data["workflow"]
    inputs = data.get("inputs", [])
    outputs = data["outputs"]
    implementation = data.get("implementation", None)
    dependencies = data.get("dependencies", [])

    workflow_ = crate.add(
        Entity(
            crate,
            identifier="#workflow",
            properties={
                "@type": "CreateAction",
                "name": workflow["name"],
                "description": workflow["description"],
                "endTime": workflow.get("endTime", None),
                "startTime": workflow.get("startTime", None),
                "resourceUsage": add_columns(
                    workflow.get("resourceUsage", []), "", crate
                ),
            },
        )
    )
    inputs_ = add_files(inputs, crate, basepath)
    outputs_ = add_tabular_files(outputs, basepath, crate)

    workflow_["result"] = outputs_
    workflow_["object"] = inputs_
    workflow_["agent"] = {"@id": workflow.get("agent", None)}

    if implementation is not None:
        workflow_["instrument"] = add_implementation(
            implementation, dependencies, crate
        )

    return set_root("mentions", workflow_, crate)


@curry
def add_contexts(contexts, crate):
    """Add the contexts to the crate"""
    # pylint: disable=unnecessary-lambda
    list(fmap(lambda x: crate.metadata.extra_contexts.append(x), contexts))
    return crate


def make_run_crate(crate):
    """Ensure the crate as Workflow Run RO-Crate"""
    id_ = "https://w3id.org/ro/wfrun/process/0.4"
    set_root("conformsTo", {"@id": id_}, crate)
    crate.add(
        Entity(
            crate,
            identifier=id_,
            properties={
                "@type": "CreativeWork",
                "name": "Process Run Crate",
                "version": "0.1",
            },
        )
    )
    return crate


@curry
def add_spec(spec, basepath, crate):
    """Add the specification section to the crate"""
    if "path" in spec:
        add_tabular_file(spec, basepath, crate)
    else:
        crate.add(
            Entity(
                crate,
                identifier="specification",
                properties={
                    "@type": ["File", "Dataset"],
                    "description": spec["description"],
                    "name": spec["name"],
                    "keywords": spec["keywords"],
                },
            )
        )
    return crate


def generate_(data, dest, basepath):
    """Generate the crate"""
    return pipe(
        ROCrate(),
        add_contexts(data["contexts"]),
        set_attr(key="description", value=data["description"]),
        make_run_crate,
        set_root("title", data["title"]),
        add_authors(data["authors"]),
        add_license(data["license"]),
        add_workflow(data, basepath),
        #     data["workflow"],
        #     data.get("inputs", []),
        #     data["outputs"],
        #     data.get("implementation", None),
        #     data.get("dependencies", []),
        #     basepath,
        # ),
        add_spec(data["specification"], basepath),
        lambda x: x.write(dest),
    )


@rocrate_cli.command(epilog=EPILOG)
def test():  # pragma: no cover
    """Run the PFHub tests

    Currently creates a stray .coverage file when running.
    """
    rocrate_cli_test()
