from .errors import DismErrors
from .interpreter import Interpreter
from .lexer import Lexer
from .parser import Parser


class DISM:
    def run(self, program: str) -> None:
        tokens = Lexer(program).lex()
        instructions, labels = Parser(tokens).parse()

        if DismErrors.had_error:
            return

        Interpreter(instructions, labels).interpret()
