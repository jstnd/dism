from enum import Enum, auto
from typing import Any


class TokenType(Enum):
    ADD = auto()
    SUB = auto()
    MUL = auto()
    MOV = auto()
    LOD = auto()
    STR = auto()
    JMP = auto()
    BEQ = auto()
    BGT = auto()
    RDN = auto()
    PTN = auto()
    HLT = auto()
    INT = auto()
    LABEL = auto()
    COLON = auto()
    EOF = auto()


class Token:
    def __init__(self, typ: TokenType, literal: Any, line: int):
        self.typ = typ
        self.literal = literal
        self.line = line

    def __str__(self):
        return f"{self.typ} ({self.literal}) : line {self.line}"
