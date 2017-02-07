#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import os
import subprocess

from .mojobackend import MojoBackend


class PythonMojoBackend(MojoBackend):

    def _launch_server_process(self, port) -> None:
        pyserver = os.path.join(self._pkg_root_dir(), "mojo-py", "rest-server", "server.py")
        if not os.path.isfile(pyserver):
            raise Exception("Could not locate %s" % pyserver)

        cmd = ["python2", pyserver, "--port", str(port)]
        print("Lauching python server: %s" % " ".join(cmd))
        self._stdout = self._make_output_file_name("out")
        self._stderr = self._make_output_file_name("err")
        self._process = subprocess.Popen(args=cmd, bufsize=0,
                                         stdout=open(self._stdout, "wb", 0),
                                         stderr=open(self._stderr, "wb", 0))
