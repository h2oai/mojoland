#!/usr/bin/env Python3
# -*- encoding: utf-8 -*-
from typing import List, Optional
import re


def parse_string_list(s: str) -> List[str]:
    assert s.startswith("[") and s.endswith("]"), "Invalid list %s" % s
    pieces = re.split(r",\s*", s[1:-1])
    res = []
    for piece in pieces:
        assert piece.startswith('"') and piece.endswith('"') and "\\" not in piece, "Unexpected piece: %s" % piece
        res.append(piece[1:-1])
    return res


def parse_string_doublelist(s: str) -> List[Optional[List[str]]]:
    assert s.startswith("[") and s.endswith("]"), "Invalid list %s" % s
    res = []  # type: List[Optional[List[str]]]
    i = 1
    while i < len(s) - 1:
        assert s[i] == "n" or s[i] == "[", "Unexpected token: %s" % s[i:]
        if s[i] == "n":
            assert s[i:i+4] == "null", "Unexpected token: %s" % s[i:]
            res.append(None)
            i += 4
        else:
            j = s.find("]", i+1)
            assert j >= i + 1, "Cannot find closing ] in string %s" % s[i:]
            res.append(parse_string_list(s[i:j+1]))
            i = j + 1
        if s[i] == ",":
            i += 1
        while s[i] == " ":
            i += 1
    return res
