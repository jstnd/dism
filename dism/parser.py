from typing import Final

from .tokens import Token, TokenType


class Instruction:
    def __init__(self, opcode: Token, *args: Token):
        self.opcode = opcode
        self.args = args

    def __str__(self):
        return f"{self.opcode.typ} {[str(arg) for arg in self.args]}"


class Parser:
    def __init__(self, tokens: list[Token]):
        self._tokens: Final = tokens

        self._instructions: list[Instruction] = []
        self._labels: dict[str, int] = {}
        self._current = 0

    def parse(self) -> tuple[list[Instruction], dict[str, int]]:
        self._instruction_list()
        return self._instructions, self._labels

    def _instruction_list(self) -> None:
        while not self._at_end():
            token = self._advance()
            match token.typ:
                case TokenType.INT | TokenType.COLON:
                    ...  # TODO: implement error
                case TokenType.LABEL:
                    if self._match(TokenType.COLON):
                        self._instructions.append(self._labeled_instruction(token))
                    else:  # TODO: implement error
                        ...
                case _:  # INSTRUCTION
                    self._instructions.append(self._instruction())

    def _instruction(self) -> Instruction:
        instruction: Token = self._previous()
        match instruction.typ:
            case TokenType.ADD: return self._add()
            case TokenType.SUB: return self._sub()
            case TokenType.MUL: return self._mul()
            case TokenType.MOV: return self._mov()
            case TokenType.LOD: return self._lod()
            case TokenType.STR: return self._str()
            case TokenType.JMP: return self._jmp()
            case TokenType.BEQ: return self._beq()
            case TokenType.BGT: return self._bgt()
            case TokenType.RDN: return self._rdn()
            case TokenType.PTN: return self._ptn()
            case TokenType.HLT: return self._hlt()
            case _: ...  # TODO: implement error

    def _labeled_instruction(self, label: Token) -> Instruction:
        self._labels[label.literal] = len(self._instructions)
        self._advance()
        return self._instruction()

    def _add(self) -> Instruction:
        opcode: Token = self._previous()
        args: list[Token] = self._get_args(3)
        return Instruction(opcode, *args)

    def _sub(self) -> Instruction:
        opcode: Token = self._previous()
        args: list[Token] = self._get_args(3)
        return Instruction(opcode, *args)

    def _mul(self) -> Instruction:
        opcode: Token = self._previous()
        args: list[Token] = self._get_args(3)
        return Instruction(opcode, *args)

    def _mov(self) -> Instruction:
        opcode: Token = self._previous()
        args: list[Token] = self._get_args(2)
        return Instruction(opcode, *args)

    def _lod(self) -> Instruction:
        opcode: Token = self._previous()
        args: list[Token] = self._get_args(3)
        return Instruction(opcode, *args)

    def _str(self) -> Instruction:
        opcode: Token = self._previous()
        args: list[Token] = self._get_args(3)
        return Instruction(opcode, *args)

    def _jmp(self) -> Instruction:
        opcode: Token = self._previous()
        args: list[Token] = self._get_args(2)
        return Instruction(opcode, *args)

    def _beq(self) -> Instruction:
        opcode: Token = self._previous()
        args: list[Token] = self._get_args(3)
        return Instruction(opcode, *args)

    def _bgt(self) -> Instruction:
        opcode: Token = self._previous()
        args: list[Token] = self._get_args(3)
        return Instruction(opcode, *args)

    def _rdn(self) -> Instruction:
        opcode: Token = self._previous()
        args: list[Token] = self._get_args(1)
        return Instruction(opcode, *args)

    def _ptn(self) -> Instruction:
        opcode: Token = self._previous()
        args: list[Token] = self._get_args(1)
        return Instruction(opcode, *args)

    def _hlt(self) -> Instruction:
        opcode: Token = self._previous()
        args: list[Token] = self._get_args(1)
        return Instruction(opcode, *args)
    
    def _get_args(self, num: int) -> list[Token]:
        args = []
        for _ in range(num):
            args.append(self._int())
        return args

    def _int(self) -> Token:
        if self._match(TokenType.INT, TokenType.LABEL):
            return self._previous()
        else:
            ...  # TODO: implement error

    def _at_end(self) -> bool:
        return self._peek().typ == TokenType.EOF

    def _peek(self) -> Token:
        return self._tokens[self._current]

    def _advance(self) -> Token:
        if not self._at_end():
            self._current += 1
        return self._previous()

    def _previous(self) -> Token:
        return self._tokens[self._current - 1]

    def _match(self, *types: TokenType) -> bool:
        for typ in types:
            if self._check(typ):
                self._advance()
                return True

        return False

    def _check(self, typ: TokenType) -> bool:
        if self._at_end():
            return False
        return self._peek().typ == typ
