from typing import Any

from .errors import DismErrors
from .tokens import TokenType, Token


class Lexer:
    instructions: dict[str, TokenType] = {
        "add": TokenType.ADD,
        "sub": TokenType.SUB,
        "mul": TokenType.MUL,
        "mov": TokenType.MOV,
        "lod": TokenType.LOD,
        "str": TokenType.STR,
        "jmp": TokenType.JMP,
        "beq": TokenType.BEQ,
        "bgt": TokenType.BGT,
        "rdn": TokenType.RDN,
        "ptn": TokenType.PTN,
        "hlt": TokenType.HLT,
    }

    def __init__(self, source: str):
        self._source = source

        self._tokens: list[Token] = []
        self._start = 0
        self._current = 0
        self._line = 1

    def lex(self) -> list[Token]:
        while not self._at_end():
            self._start = self._current
            self._lex()

        self._add_token(TokenType.EOF)
        return self._tokens

    def _lex(self) -> None:
        c: str = self._advance()
        match c:
            case " " | "\r" | "\t": pass
            case "\n": self._line += 1
            case ":": self._add_token(TokenType.COLON)
            case "#": self._label()
            case ";": self._comment()
            case "-":
                if self._peek().isdigit():
                    self._number()
                else:
                    DismErrors.error(self._line, f"Syntax error: Unexpected character '-'")
            case _ if c.isalpha(): self._instruction()
            case _ if c.isdigit(): self._number()
            case _: DismErrors.error(self._line, f"Syntax error: Unexpected character '{c}'")

    def _at_end(self) -> bool:
        return self._current >= len(self._source)

    def _add_token(self, typ: TokenType, literal: Any = None) -> None:
        text: str = self._source[self._start:self._current]
        self._tokens.append(Token(typ, text, literal, self._line))

    def _advance(self) -> str:
        c: str = self._source[self._current]
        self._current += 1
        return c

    def _peek(self) -> str:
        if self._at_end():
            return "\0"
        return self._source[self._current]

    def _previous(self) -> str:
        return self._source[self._current - 1]

    def _label(self) -> None:
        while self._peek().isalnum() and not self._at_end():
            self._advance()

        self._add_token(TokenType.LABEL, self._source[self._start:self._current])

    def _comment(self) -> None:
        while self._peek() != "\n" and not self._at_end():
            self._advance()

    def _instruction(self) -> None:
        while self._peek().isalnum() and not self._at_end():
            self._advance()

        text: str = self._source[self._start:self._current]
        typ: TokenType = Lexer.instructions.get(text)
        if typ is None:
            DismErrors.error(self._line, f"Syntax error: Unexpected character(s) '{text}'")

        self._add_token(typ)

    def _number(self) -> None:
        while self._peek().isdigit():
            self._advance()

        self._add_token(TokenType.INT, int(self._source[self._start:self._current]))
