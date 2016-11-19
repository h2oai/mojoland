#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import atexit
import os
import re
import subprocess
import time
from typing import List, Dict, Optional

import requests
import h2o
from h2o.backend import H2OLocalServer


class MojoServer:
    """"""
    _TIME_TO_START = 3  # maximum time to wait until server starts (in seconds)

    @staticmethod
    def get():
        if not hasattr(MojoServer, "_instance"):
            MojoServer._instance = MojoServer()
        return MojoServer._instance


    def __init__(self):
        self._port = -1          # type: int
        self._output_dir = None  # type: Optional[str]
        self._stdout = None      # type: Optional[str]
        self._stderr = None      # type: Optional[str]
        self._process = None     # type: Optional[subprocess.Popen]
        self._start()
        if self._process:
            atexit.register(self.shutdown)


    def load_model(self, mojofile: str) -> str:
        """Load the specified mojofile, and return its model id."""
        return self._request("GET /loadmojo", params={"file": mojofile})


    def get_model_api(self, model_id: str) -> List[str]:
        return self._request("GET /mojos/%s" % model_id).split("\n")


    def invoke_method(self, model_id: str, method: str, params: Dict) -> str:
        return self._request("GET /mojos/%s/%s" % (model_id, method), params=params)


    def shutdown(self):
        self._request("POST /shutdown")


    def unload_model(self, model_id: str) -> None:
        self._request("DELETE /mojos/%s" % model_id)


    @property
    def working_dir(self) -> str:
        if not self._output_dir:
            self._make_output_file_name("")
            assert self._output_dir
        return self._output_dir


    #-------------------------------------------------------------------------------------------------------------------
    # Private
    #-------------------------------------------------------------------------------------------------------------------

    def _start(self) -> None:
        for port in range(54320, 54310, -2):
            if self._check_if_mojoserver_is_running(port):
                print("Connected to MojoServer on port %d" % port)
                self._port = port
                return
            else:
                self._launch_server_process(port)
                print("Starting server on port %d.." % port, end="")
                if self._check_if_server_has_started(port):
                    print("ok.")
                    self._port = port
                    return
                else:
                    self._process = None
        raise RuntimeError("Failed to start MojoServer. Check logs at\n  %s\n  %s" %
                           (self._stdout, self._stderr))


    def _check_if_mojoserver_is_running(self, port: int):
        try:
            resp = requests.get("http://localhost:%d/healthcheck" % port, timeout=2)
            return resp.status_code == 418
        except requests.RequestException:
            return False


    def _pkg_root_dir(self):
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        assert root_dir.endswith("mojoland"), "Unexpected grandparent directory %s" % root_dir
        return root_dir


    def _make_output_file_name(self, suffix: str) -> str:
        if not self._output_dir:
            mojoland_dir = self._pkg_root_dir()
            self._output_dir = os.path.join(mojoland_dir, "temp", str(int(time.time() * 1000)))
            if not os.path.exists(self._output_dir):
                os.makedirs(self._output_dir)
        return os.path.join(self._output_dir, "mojo-server-%s.log" % suffix)


    def _launch_server_process(self, port) -> None:
        jar = os.path.join(self._pkg_root_dir(), "mojo-java", "build", "libs", "mojo-server.jar")
        if not os.path.isfile(jar):
            raise Exception("Could not locate JAR %s" % jar)

        getjava = getattr(H2OLocalServer, "_find_java")
        if not getjava:
            raise Exception("Method H2OLocalServer._find_java() is no longer accessible")
        java = getjava()

        cmd = [java, "-ea", "-jar", jar, "--port", str(port)]
        self._stdout = self._make_output_file_name("out")
        self._stderr = self._make_output_file_name("err")
        self._process = subprocess.Popen(args=cmd, stdout=open(self._stdout, "w"), stderr=open(self._stderr, "w"))


    def _check_if_server_has_started(self, port: int) -> bool:
        giveup_time = time.time() + self._TIME_TO_START
        regex1 = re.compile(r"MojoServer started on port (\d+)")
        regex2 = re.compile(r"MojoServer failed to start on port (\d+)")
        while time.time() < giveup_time:
            if self._process.poll() is not None:
                print("Process terminated with return code %d" % self._process.returncode)
                return False
            with open(self._stdout, "r") as f:
                for line in f:
                    mm = re.match(regex1, line)
                    if mm is not None:
                        assert port == int(mm.group(1)), "Ports mismatch: expected %d found %s" % (port, mm.group(1))
                        return True
                    mm = re.match(regex2, line)
                    if mm is not None:
                        print("port already in use")
                        return False
            print(".", end="", flush=True)
            time.sleep(0.2)
        print("Server wasn't able to start in %.2f seconds" % (time.time() - giveup_time + self._TIME_TO_START))
        return False


    def _request(self, endpoint: str, params: Dict = None):
        mm = re.match(r"(GET|POST|DELETE) ((?:/[\w~.]+)+)", endpoint)
        if mm:
            method = mm.group(1)
            path = mm.group(2)
            url = "http://localhost:%d%s" % (self._port, path)
        else:
            raise Exception("Invalid endpoint %s" % endpoint)
        # Make the request
        resp = requests.request(method, url, params=params)
        if resp.status_code == 200 or resp.status_code == 202:
            return resp.text.strip()
        else:
            raise Exception("Error %d: %s\n>> Request: %s\n>> Params:  %r" %
                            (resp.status_code, resp.text, endpoint, params))
