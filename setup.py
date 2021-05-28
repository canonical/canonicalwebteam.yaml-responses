#! /usr/bin/env python3

from setuptools import setup

setup(
    name="canonicalwebteam.yaml-responses",
    version="1.2.0",
    author="Canonical Webteam",
    url="https://github.com/canonical-webteam/yaml-responses",
    packages=["canonicalwebteam.yaml_responses"],
    description=(
        "Functions to read from yaml files to provide"
        "generic responses to URLs in Django and Flask"
    ),
    install_requires=["pyyaml", "yamlloader"],
    extras_require={"django": ["Django"], "flask": ["flask"]},
    tests_require=["Django", "flask", "pyyaml", "yamlloader"],
    test_suite="tests",
)
