#! /usr/bin/env python3.9
from setuptools import setup

setup(
    name="plpipe",
    version="0.1",
    packages=["plpipe"],
    entry_points={
        "console_scripts": [
            "pl-phase = plpipe.pl_phase:main",
            "pl-line = plpipe.pl_line:main",
            "pl-surf = plpipe.pl_surf:main",
        ],
    },
)

