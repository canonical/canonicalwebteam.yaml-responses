#! /usr/bin/env python3

from setuptools import setup

setup(
    name="canonicalwebteam.yaml-responses",
    version="1.0.1",
    author="Canonical Webteam",
    url="https://github.com/canonical-webteam/yaml-responses",
    packages=["canonicalwebteam.yaml_responses"],
    description=(
        "Functions to read from yaml files to provide"
        "generic responses to URLs in Django and Flask"
    ),
    install_requires=["pyyaml"],
    extras_require={
        "django": ["Django"],
        "flask": ["flask", "yamlordereddictloader"],
    },
    tests_require=["Django", "flask", "yamlordereddictloader"],
    test_suite="tests",
)
