#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


def init(autoreset: bool = False, convert: bool = None, strip: bool = None, wrap: bool = True) -> None: ...

def deinit() -> None: ...

def reinit() -> None: ...


class Fore:
    BLACK = ...            # type: str
    BLUE = ...             # type: str
    CYAN = ...             # type: str
    GREEN = ...            # type: str
    LIGHTBLACK_EX = ...    # type: str
    LIGHTBLUE_EX = ...     # type: str
    LIGHTCYAN_EX = ...     # type: str
    LIGHTGREEN_EX = ...    # type: str
    LIGHTMAGENTA_EX = ...  # type: str
    LIGHTRED_EX = ...      # type: str
    LIGHTWHITE_EX = ...    # type: str
    LIGHTYELLOW_EX = ...   # type: str
    MAGENTA = ...          # type: str
    RED = ...              # type: str
    RESET = ...            # type: str
    WHITE = ...            # type: str
    YELLOW = ...           # type: str



class Style:
    BRIGHT = ...     # type: str
    DIM = ...        # type: str
    NORMAL = ...     # type: str
    RESET_ALL = ...  # type: str



class Cursor:

    @staticmethod
    def BACK(x: int) -> str: ...

    @staticmethod
    def DOWN(x: int) -> str: ...

    @staticmethod
    def FORWARD(x: int) -> str: ...

    @staticmethod
    def POS() -> str: ...

    @staticmethod
    def UP(x: int) -> str: ...
