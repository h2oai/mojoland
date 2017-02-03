#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from typing import Dict
from .mojobackend import MojoBackend
from .java import JavaMojoBackend
from .python import PythonMojoBackend


_instances = {}  # type: Dict[str, MojoBackend]

def get_backend(name: str) -> MojoBackend:
    if name not in _instances:
        if name == "java":
            server = JavaMojoBackend()
        elif name == "python":
            server = PythonMojoBackend()
        else:
            raise RuntimeError("Unknown backendL %s" % name)
        _instances[name] = server
    return _instances[name]
