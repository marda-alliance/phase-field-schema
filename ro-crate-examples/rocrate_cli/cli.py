from rocrate.rocrate import ROCrate
from rocrate.model.person import Person
from rocrate.model.entity import Entity
from rocrate.model.computationalworkflow import ComputationalWorkflow
from rocrate.model.contextentity import ContextEntity
from frictionless import Schema, Resource
import yaml
import toolz
from toolz.curried import curry, pipe
from toolz.curried import map as fmap
import click
import os
import urllib

# Helpful webpages:
#   - https://www.researchobject.org/workflow-run-crate/profiles/process_run_crate/
#   - https://biotools.readthedocs.io/en/latest/curators_guide.html#tool-type
#   - https://github.com/ResearchObject/ro-terms/tree/master/workflow-run


EPILOG = "See the documentation in the README"

@click.group(epilog=EPILOG)
def rocrate_cli():
    """Generate an ro-crate from a phase field example"""

@rocrate_cli.command(epilog=EPILOG)
@click.argument(
    "config",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    default="./ro-crate-config.yaml"
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
    crate = generate_(data, dest, os.path.dirname(config))


def read_yaml(filepath):
    with open(filepath, 'r') as file:
        yaml_content = yaml.safe_load(file)
    return yaml_content


@curry
def set_value(obj, key, value):
    obj[key] = value
    return obj


@curry
def set_attr(obj, key, value):
    setattr(obj, key, value)
    return obj


@curry
def crateadd(crate, thing):
    return crate.add(thing)


@curry
def add_authors(authors, crate):
    return pipe(
        authors,
        fmap(lambda x: crate.add(
            Person(
                crate,
                x['orcid'],
                properties=dict(
                    name=x['name'],
                    affiliation=x['affiliation']
                )
            )
        )),
        list,
        set_root("author", crate=crate)
    )


@curry
def add_license(license, crate):
    return pipe(
        license,
        lambda x: crate.add(Entity(
            crate,
            identifier=license['identifier'],
            properties={
                "@type": "CreativeWork",
                "name": license["name"],
                "description": license["description"],
                "url": license["url"]
           }
        )),
        set_attr(crate, "license")
    )


def isabs(path):
    """Check if a path is an absolute or relative path"""
    return (
        urllib.parse.urlparse(str(path)).scheme in ("http", "https", "file")
    ) or os.path.isabs(path)


def makeabs(basepath, filename):
    if isabs(filename):
        return filename
    else:
        return os.path.join(basepath, filename)
        
@curry
def add_files(files, crate, basepath):
    return list(fmap(lambda x: crate.add_file(
        makeabs(basepath, x["path"]),
        fetch_remote=x["download"],        
        properties=dict(
            name=x["name"],
            encodingFormat=x["encodingFormat"],
            description=x["description"],
            variableMeasured=add_columns(x.get("columns", []), x["path"], crate)
        )), files))


@curry
def add_column(path, crate, column):
    identifier = path + "#" + column['identifier']
    crate.add_jsonld({
        "@id": identifier,
        "@type": "PropertyValue",
        "unitCode": column.get("unit", None),
        "name": column.get("name", column.get("identifier", None)),
        "description": column["description"],
        "value": column.get("value", None)
    })
    return {"@id": identifier}
    


@curry
def add_columns(columns, path, crate):
    return list(fmap(
        add_column(path, crate),
        columns
    ))

                
@curry
def add_tabular_file(file, basepath, crate):
    if file["type"] == "directory":
        return crate.add_directory(
            makeabs(basepath, file["path"]),
            properties={
                "description": file["description"],
                "encodingFormat": file["encodingFormat"],
                "name": file["name"],
                "variableMeasured": add_columns(file.get("columns", []), file["path"], crate),
            }
        )
    else:
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
                "variableMeasured": add_columns(file.get("columns", []), file["path"], crate),
            }
        )

@curry
def add_tabular_files(files, basepath, crate):
    return list(fmap(add_tabular_file(basepath=basepath, crate=crate), files))


@curry
def set_root(key, value, crate):
    crate.root_dataset[key] = value
    return crate


@curry
def add_dependency(crate, dependency):
    return crate.add(Entity(
        crate,
        identifier=dependency["identifier"],
        properties={
            "@type": "SoftwareApplication",
            "description": dependency["description"],
            "name": dependency["name"],
            "url": dependency["url"],
            "version": dependency["version"]
         }
    ))
    

@curry
def add_implementation(implementation, dependencies, crate):
    implementation_ = crate.add(Entity(
        crate,
        identifier=implementation["identifier"],
        properties={
            "@type": "SoftwareApplication",
            "conformsTo": "https://bioschemas.org/profiles/ComputationalTool/1.0-RELEASE",
            "description": implementation["description"],
            "name": implementation["name"],
            "applicationCategory": implementation["applicationCategory"],
            "url": implementation["codeRepository"],
            "codeRepository": implementation["codeRepository"],
            "programmingLanguage": implementation["programmingLanguage"]
         }
    ))

    implementation_["softwareRequirements"] = list(fmap(add_dependency(crate), dependencies))
    
    return implementation_


@curry
def add_workflow(workflow, inputs, outputs, implementation, dependencies, basepath, crate):
    workflow_ = crate.add(Entity(
        crate,
        identifier="#workflow",
        properties={
            "@type": "CreateAction",
            "name": workflow["name"],
            "description": workflow["description"],
            "endTime": workflow.get("endTime", None),
            "startTime": workflow.get("startTime", None),
            "resourceUsage": add_columns(workflow.get("resourceUsage", []), "", crate)
        }
    ))
    inputs_ = add_files(inputs, crate, basepath)
    outputs_ = add_tabular_files(outputs, basepath, crate)

    workflow_["result"] = outputs_
    workflow_["object"] = inputs_
    workflow_["agent"] = {"@id": workflow.get("agent", None)}

    if implementation is not None:
        workflow_["instrument"] = add_implementation(implementation, dependencies, crate)

    
    return set_root("mentions", workflow_, crate)



@curry
def add_contexts(contexts, crate):
    list(fmap(
        lambda x: crate.metadata.extra_contexts.append(x),
        contexts
    ))
    return crate


def make_run_crate(crate):
    id_ = "https://w3id.org/ro/wfrun/process/0.4"
    set_root("conformsTo", {"@id": id_}, crate)
    crate.add(Entity(
        crate,
        identifier=id_,
        properties={
            "@type": "CreativeWork",
            "name": "Process Run Crate",
            "version": "0.1"
        }
    ))
    return crate

@curry
def add_spec(spec, basepath, crate):
    if "path" in spec:
        spec_ = add_tabular_file(spec, basepath, crate)
    else:
        crate.add(Entity(
        crate,
            identifier="specification",
            properties={
                "@type": ["File", "Dataset"],
                "description": spec["description"],
                "name": spec["name"],
                "keywords": spec["keywords"],
            }
        ))
    return crate

def debug(x):
    print('debug:', x)
#    import ipdb; ipdb.set_trace();
    return x

def generate_(data, dest, basepath):
    return pipe(
        ROCrate(),
        add_contexts(data['contexts']),
        set_attr(key='description', value=data['description']),
        make_run_crate,
        set_root('title', data['title']),
        add_authors(data['authors']),
        add_license(data['license']),
        add_workflow(
            data['workflow'],
            data.get('inputs', []),
            data['outputs'],
            data.get("implementation", None),
            data.get("dependencies", []),
            basepath
        ),
        add_spec(data["specification"], basepath),
        lambda x: x.write(dest)
    )


