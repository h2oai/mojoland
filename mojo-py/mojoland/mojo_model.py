#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from mojoland.backend import MojoServer


class MojoModel:

    def __init__(self, filename: str, major_version: int):
        server = MojoServer.get()
        self._id = server.load_model(filename)
        self._majver = major_version


    def call(self, method, *args):
        server = MojoServer.get()
        params = {"arg%d" % i: arg for i, arg in enumerate(args, 1)}
        return server.invoke_method(self._id, method, params)


    def close(self):
        MojoServer.get().unload_model(self._id)
