#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from typing import Dict, Generator, Iterator, List, Optional, Tuple

from mojoland.backend import MojoServer
from mojoland.recipes.cookbook import v0_simple_params, v0_multi_params
from mojoland.utils import parse_string_list, parse_string_doublelist

Commands = Iterator[Tuple[str, ...]]


class MojoModel:

    def __init__(self, filename: str, major_version: int) -> None:
        server = MojoServer.get()
        self._id = server.load_model(filename)
        self._majver = major_version
        self._nfeatures = None  # type: Optional[int]
        self._colnames = None   # type: Optional[List[str]]
        self._domains = None    # type: Optional[List[Optional[List[str]]]]
        self._npreds = None     # type: Optional[int]
        self._enumsmap = None   # type: Optional[Dict[int, Dict[str, int]]]


    def call(self, method: str, *args: str) -> str:
        server = MojoServer.get()
        params = {"arg%d" % i: arg for i, arg in enumerate(args, 1)}
        return server.invoke_method(self._id, method, params)


    def close(self) -> None:
        MojoServer.get().unload_model(self._id)


    #-------------------------------------------------------------------------------------------------------------------
    # Meta-properties
    #-------------------------------------------------------------------------------------------------------------------

    @property
    def nfeatures(self) -> int:
        """
        Number of features in the model.

        This is the size of the `data` array for the scoring function.
        """
        if self._nfeatures is None:
            method = "nfeatures"  # version-dependent
            self._nfeatures = int(self.call(method))
        return self._nfeatures


    @property
    def colnames(self) -> List[str]:
        """
        Names of all columns in the input dataset.

        The first `nfeatures` columns are the features columns, but there may
        be additional ones (for example response, weights, offsets, etc).
        """
        if self._colnames is None:
            method = "getNames"  # version-dependent
            self._colnames = parse_string_list(self.call(method))
        return self._colnames


    @property
    def domains(self) -> List[Optional[List[str]]]:
        """
        Domain mappings for all categorical columns.

        If a column `i` in the input dataset was categorical, then `domains[i]`
        will contain all categorical levels for that column, in the order they
        were mapped to integers. For example, if `domains[i] = ["cat", "dog",
        "frog"]`, then in the i-th column "cat"s should be mapped to 0, "dog"s
        should mapped to 1, and "frog"s mapped to 2.

        If a column `i` is not categorical, then the corresponding entry in
        the domains list will be `None`.
        """
        if self._domains is None:
            method = "getDomainValues~"  # version-dependent
            self._domains = parse_string_doublelist(self.call(method))
        return self._domains


    @property
    def npredictions(self) -> int:
        if self._npreds is None:
            method = "getPredsSize~"  # version-dependent
            self._npreds = int(self.call(method))
        return self._npreds


    @property
    def enums_map(self) -> Dict[int, Dict[str, int]]:
        if self._enumsmap is None:
            self._enumsmap = {}
            for i, domain in self.domains:
                if domain is not None:
                    self._enumsmap[i] = {cat: j for j, cat in domain}
        return self._enumsmap


    def prepare_row(self, row: List[str]):
        """Modifies `row` in-place to map all enum columns to integer codes."""
        for i, emap in self.enums_map:
            row[i] = str(emap.get(row[i], "NaN"))


    #-------------------------------------------------------------------------------------------------------------------
    # Nibbles helpers
    #-------------------------------------------------------------------------------------------------------------------

    def simple_params_nibble(self) -> Commands:
        if self._majver >= 0:
            yield from v0_simple_params()


    def multi_params_nibble(self) -> Commands:
        if self._majver >= 0:
            yield from v0_multi_params(self)


    def scores0(self, datagen: Iterator[List[str]]):
        predictions = repr([0] * self.npredictions)
        for row in datagen:
            self.prepare_row(row)
            yield ("score0~dada", "[%s]" % ",".join(row[:self.nfeatures]), predictions)

    def scores1(self, datagen: Iterator[List[str]]):
        predictions = repr([0] * self.npredictions)
        for i, row in enumerate(datagen):
            self.prepare_row(row)
            yield ("score0~dadda", "[%s]" % ",".join(row[:self.nfeatures]), i, predictions)

    def scores2(self):
        """Score against some irregular data (including NAs)."""
        method = "score0~dada"
        n = self.nfeatures
        predictions = repr([0] * self.npredictions)

        def score(r):
            return method, "[%s]" % ",".join(r), predictions

        yield score(["NaN"] * n)
        yield score(["0"] * n)
        yield score([str(-x) for x in range(n)])
        yield score([str(x) for x in range(n + 1)])
        yield score([str(x) for x in range(n - 1)])
        for i in range(n - 1):
            row = [str(x * 1000) for x in range(i)] + ["NaN"] + [str(x) for x in range(i + 2, n)]
            yield score(row)
        for i in range(10, 201, 10):
            row = ["%de%d" % (x + 1, i) for x in range(n)]
            yield score(row)
        predictions = "[0]"
        yield score(["0"] * n)
