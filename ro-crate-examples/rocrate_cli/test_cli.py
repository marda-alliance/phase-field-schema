"""Test function for the RO-Crate generator
"""

import os

from click.testing import CliRunner

from .cli import generate, rocrate_cli


def test_cli():
    """Test top-level of CLI tool"""
    runner = CliRunner()
    result = runner.invoke(rocrate_cli)
    assert result.exit_code == 0


def test_generate_simple(tmpdir):
    """Test running a simple ro-crate generation"""
    generate_helper(tmpdir, "simple")


def test_generate_fipy(tmpdir):
    """Test running a simple ro-crate generation"""
    generate_helper(tmpdir, "fipy")


def test_generate_prismspf(tmpdir):
    """Test running a simple ro-crate generation"""
    generate_helper(tmpdir, "prisms-pf")


def generate_helper(tmpdir, example_name):
    """generic tester"""
    runner = CliRunner()
    base = os.path.split(__file__)[0]
    yaml_path = os.path.join(base, "..", example_name, "config.yaml")
    result = runner.invoke(
        generate, [yaml_path, "--dest", os.path.join(tmpdir, "crate")]
    )
    assert result.exit_code == 0
    assert os.path.exists(os.path.join(tmpdir, "crate", "ro-crate-metadata.json"))


def test_dir(tmpdir):
    """Directory already exists"""
    runner = CliRunner()
    base = os.path.split(__file__)[0]
    yaml_path = os.path.join(base, "..", "simple", "config.yaml")
    result = runner.invoke(generate, [yaml_path, "--dest", os.path.join(tmpdir)])
    print(result.output)
    assert result.exit_code == 2
