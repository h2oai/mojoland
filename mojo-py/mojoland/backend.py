#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import os
import re
import subprocess
import time
from typing import List, Dict

import requests
from h2o.backend import H2OLocalServer


class MojoServer:
    """"""
    _TIME_TO_START = 5  # maximum time to wait until server starts (in seconds)


    def __init__(self):
        self._port = 0
        self._stdout = self._make_output_file_name("out")
        self._stderr = self._make_output_file_name("err")
        self._process = self._launch_server_process()
        self._wait_for_server_to_start()


    def load_model(self, mojofile: str) -> str:
        """Load the specified mojofile, and return its model id."""
        return self._request("GET /loadmojo", params={"file": mojofile})


    def get_model_api(self, model_id: str) -> List[str]:
        return self._request("GET /mojos/%s" % model_id).split("\n")


    def shutdown(self):
        return self._request("POST /shutdown")


    #-------------------------------------------------------------------------------------------------------------------
    # Private
    #-------------------------------------------------------------------------------------------------------------------

    def _make_output_file_name(self, suffix: str) -> str:
        mojoland_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        assert mojoland_dir.endswith("mojoland"), "Unexpected grandparent directory %s" % mojoland_dir
        output_dir = os.path.join(mojoland_dir, "temp", str(int(time.time() * 1000)))
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        return os.path.join(output_dir, "mojo-server-%s.log" % suffix)


    def _launch_server_process(self) -> subprocess.Popen:
        jar = os.path.join(os.path.dirname(__file__), "..", "..", "mojo-java", "build", "libs", "mojo-server.jar")
        if not os.path.isfile(jar):
            raise RuntimeError("Could not locate JAR %s" % jar)

        getjava = getattr(H2OLocalServer, "_find_java")
        if not getjava:
            raise RuntimeError("Method H2OLocalServer._find_java() is no longer accessible")
        java = getjava()

        cmd = [java, "-ea", "-jar", jar]
        return subprocess.Popen(args=cmd, stdout=open(self._stdout, "w"), stderr=open(self._stderr, "w"))


    def _wait_for_server_to_start(self) -> None:
        giveup_time = time.time() + self._TIME_TO_START
        while time.time() < giveup_time:
            if self._process.poll() is not None:
                raise Exception("Server process terminated with return code %d\n"
                                "Check the log file %s" % (self._process.returncode, self._stdout))
            if self._scrape_process_output():
                print()
                return
            print(".", end="", flush=True)
            time.sleep(0.2)
        raise Exception("Server wasn't able to start in %.2f seconds"
                        % (time.time() - giveup_time + self._TIME_TO_START))


    def _scrape_process_output(self) -> bool:
        regex = re.compile(r"MojoServer started on port (\d+)")
        with open(self._stdout, "r") as f:
            for line in f:
                mm = re.match(regex, line)
                if mm is not None:
                    self._port = int(mm.group(1))
                    return True
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
        if resp.status_code == 200:
            return resp.text.strip()
        else:
            raise Exception("Error %d: %s" % (resp.status_code, resp.text))
