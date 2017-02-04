#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
#
#  For now this is python-2 only, because h2omojo package is not compatible with Python3
#
from __future__ import division, print_function
import argparse
import traceback
import urlparse

# this is replaced with `http.server` in Python3
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

import h2omojo


shutdown_requested = False

class MojoStore(object):

    def __init__(self):
        self._store = {}
        self._index = 0

    def add_model(self, model):
        self._index += 1
        self._store[str(self._index)] = model
        return str(self._index)

    def get_model(self, index):
        return self._store.get(index, None)

    def del_model(self, index):
        del self._store[index]


mojo_store = MojoStore()


class MojoHandlers(BaseHTTPRequestHandler):

    def do_GET(self):
        req = urlparse.urlparse(self.path)
        params = urlparse.parse_qs(req.query)
        pathparts = req.query.split("/")
        try:
            if req.path == "/healthcheck":
                return self.handle_healthcheck()
            if req.path == "/loadmojo":
                return self.handle_load_mojo(params.get("file"))
            if pathparts[0] == "mojos" and len(pathparts) == 2:
                mojo_id = pathparts[1]
                return self.handle_mojo_api(mojo_id)
            if pathparts[0] == "mojos" and len(pathparts) == 3:
                mojo_id = pathparts[1]
                method_name = pathparts[2]
                return self.handle_mojo_method(mojo_id, method_name, params)
            self.send_error(404, "Unrecognized endpoint %s" % self.path)
        except Exception as e:
            self.send_error(500, "Exception: %s\n\n%s" % (e, traceback.format_exc()))


    def do_POST(self):
        try:
            if self.path == "/shutdown":
                return self.handle_shutdown()
            self.send_error(404, "Unrecognized endpoint %s" % self.path)
        except Exception as e:
            self.send_error(500, "Exception: %s\n\n%s" % (e, traceback.format_exc()))


    def do_DELETE(self):
        pathparts = self.path.split("/")
        try:
            assert pathparts[0] == "/"
            if len(pathparts) == 3 and pathparts[1] == "mojos":
                mojo_id = pathparts[2]
                return self.handle_unload_mojo(mojo_id)
            self.send_error(404, "Unrecognized endpoint %s" % self.path)
        except Exception as e:
            self.send_error(500, "Exception: %s\n\n%s" % (e, traceback.format_exc()))


    def send_error(self, errorCode, message=""):
        self.send_response(errorCode)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(message)


    def handle_healthcheck(self):
        """Handler for `GET /healthcheck`"""
        self.send_response(418)
        self.end_headers()


    def handle_shutdown(self):
        """Handler for `POST /shutdown`"""
        global shutdown_requested
        shutdown_requested = True
        self.send_response(200)
        self.end_headers()


    def handle_load_mojo(self, filename):
        """Handler for `GET /loadmojo?file=...`"""
        if not filename:
            self.send_error(404, "Parameter {file} is missing")
            return

        # Load the mojo...
        model = h2omojo.load_mojo_model(filename)
        id = mojo_store.add_model(model)

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(id)


    def handle_unload_mojo(self, mojo_id):
        """Handler for `DELETE /mojos/{mojo_id}`"""
        mojo_store.del_model(mojo_id)
        self.send_response(200)
        self.end_headers()


    def handle_mojo_api(self, mojo_id):
        """
        Handler for `GET /mojos/{model_id}`

        Returns mojo's public API: list of methods supported together with their
        argument types. More specifically, the response will be in plain text format
        each line having a single api method in Java traditional form::

            returnType methodName(arg1Type, ..., argNType);

        The only difference is that ``methodName``s are mangled in case
        they are overloaded in the mojo's class.
        """
        model = mojo_store.get_model(mojo_id)
        if model is None:
            self.send_error(404, "Model %s not found" % mojo_id)
            return

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        #
        # Detect the set of methods which the MOJO supports, and send their list
        # back to the client, eg:
        #
        # self.wfile.write("double score(double[]);")
        #


    def handle_mojo_method(self, mojo_id, method, params):
        """
        Handler for `GET /mojos/{model_id}/{method}?arg1=...&...&argN=...`

        This will execute ``method`` on previously loaded model ``model_id``, passing
        arguments ``arg1``, ..., ``argN``. The name of the method must be
        exactly as given by the first endpoint. In particular, if the method is
        overloaded, then this name will be mangled to make it unique.

        The endpoint will produce a plain text file with the invoked method's
        return result stringified.
        """
        args = [params["arg%d" % i] for i in range(1, len(params) + 1)]
        model = mojo_store.get_model(mojo_id)
        if model is None:
            self.send_error(404, "Model %s not found" % mojo_id)

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        #
        # Invoke ``method`` on the ``model``, passing arguments ``args``.
        # Then stringify the results and return back to the caller.
        #
        # self.wfile.write("...")
        #



def start_server(port):
    try:
        server = HTTPServer(("", port), MojoHandlers)
        print("Started Mojo-REST server on port %d" % port)
        print("MojoBackend started on port %d" % port)
        while not shutdown_requested:
            server.handle_request()
        print("Server shut down at user's request.")
    except KeyboardInterrupt:
        print("Ctrl+C pressed, shutting down")
        server.socket.close()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Server for providing REST API access to Python MOJOs")
    parser.add_argument("--port", help="Port on which to run the server", default=54299)
    args = parser.parse_args()

    start_server(int(args.port))
