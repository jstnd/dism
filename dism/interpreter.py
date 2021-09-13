from .parser import Instruction
from .tokens import Token, TokenType

NUM_REGISTERS = 8
DATA_SIZE = 64 * 1024  # 64KB


class Interpreter:
    def __init__(self, instructions: list[Instruction], labels: dict[str, int]):
        self._instructions = instructions
        self._labels = labels

        self._PC = 0
        self._R: list[int] = [0] * NUM_REGISTERS
        self._M: list[int] = [0] * DATA_SIZE

    def interpret(self) -> None:
        while True:
            self._execute(self._instructions[self._PC])

    def _execute(self, instruction: Instruction) -> None:
        args: list[int] = self._resolve_args(instruction.args)
        match instruction.opcode.typ:
            case TokenType.ADD: self._add(args)
            case TokenType.SUB: self._sub(args)
            case TokenType.MUL: self._mul(args)
            case TokenType.MOV: self._mov(args)
            case TokenType.LOD: self._lod(args)
            case TokenType.STR: self._str(args)
            case TokenType.JMP: self._jmp(args)
            case TokenType.BEQ: self._beq(args)
            case TokenType.BGT: self._bgt(args)
            case TokenType.RDN: self._rdn(args)
            case TokenType.PTN: self._ptn(args)
            case TokenType.HLT: self._hlt(args)
            case _:
                ...  # TODO: implement error

    def _resolve_args(self, args: tuple[Token, ...]) -> list[int]:
        new_args: list[int] = []

        for arg in args:
            if arg.typ == TokenType.LABEL:
                new_args.append(self._labels[arg.literal])
            else:
                new_args.append(arg.literal)

        return new_args

    def _add(self, args: list[int]) -> None:  # add d s1 s2 => R[d] <- R[s1] + R[s2]
        self._R[args[0]] = self._R[args[1]] + self._R[args[2]]
        self._PC += 1

    def _sub(self, args: list[int]) -> None:  # sub d s1 s2 => R[d] <- R[s1] - R[s2] (R[d] <- 0 when R[s2] > R[s1])
        if self._R[args[2]] > self._R[args[1]]:
            self._R[args[0]] = 0
        else:
            self._R[args[0]] = self._R[args[1]] - self._R[args[2]]

        self._PC += 1

    def _mul(self, args: list[int]) -> None:  # mul d s1 s2 => R[d] <- R[s1] * R[s2]
        self._R[args[0]] = self._R[args[1]] * self._R[args[2]]
        self._PC += 1

    def _mov(self, args: list[int]) -> None:  # mov d n => R[d] <- n
        self._R[args[0]] = args[1]
        self._PC += 1

    def _lod(self, args: list[int]) -> None:  # lod d s i => R[d] <- M[R[s] + i]
        self._R[args[0]] = self._M[self._R[args[1]] + args[2]]
        self._PC += 1

    def _str(self, args: list[int]) -> None:  # str d i s => M[R[d] + i] <- R[s]
        self._M[self._R[args[0]] + args[1]] = self._R[args[2]]
        self._PC += 1

    def _jmp(self, args: list[int]) -> None:  # jmp s i => PC <- R[s] + i
        self._PC = self._R[args[0]] + args[1]

    def _beq(self, args: list[int]) -> None:  # beq s1 s2 n => If R[s1] = R[s2] then PC <- n
        if self._R[args[0]] == self._R[args[1]]:
            self._PC = args[2]
        else:
            self._PC += 1

    def _bgt(self, args: list[int]) -> None:  # bgt s1 s2 n => If R[s1] > R[s2] then PC <- n
        if self._R[args[0]] > self._R[args[1]]:
            self._PC = args[2]
        else:
            self._PC += 1

    def _rdn(self, args: list[int]) -> None:  # rdn d => Read natural number from screen into R[d]
        self._R[args[0]] = int(input("Enter a natural number: "))
        self._PC += 1

    def _ptn(self, args: list[int]) -> None:  # ptn s => Print natural number R[s] to screen
        print(self._R[args[0]])
        self._PC += 1

    def _hlt(self, args: list[int]) -> None:  # hlt s => Halt the DISM with code R[s]
        print(f"Simulation completed with code {self._R[args[0]]} at PC={self._PC}.")
        exit()
