#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import os
import subprocess

from .mojobackend import MojoBackend


class JavaMojoBackend(MojoBackend):

    def _launch_server_process(self, port) -> None:
        jar = os.path.join(self._pkg_root_dir(), "mojo-java", "build", "libs", "mojo-server.jar")
        if not os.path.isfile(jar):
            raise Exception("Could not locate JAR %s" % jar)

        cmd = ["java", "-ea", "-jar", jar, "--port", str(port)]
        self._stdout = self._make_output_file_name("out")
        self._stderr = self._make_output_file_name("err")
        self._process = subprocess.Popen(args=cmd, stdout=open(self._stdout, "w"), stderr=open(self._stderr, "w"))

