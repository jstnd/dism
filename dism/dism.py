from .lexer import Lexer


class DISM:
    def run(self, program: str) -> None:
        tokens = Lexer(program).lex()

        for token in tokens:
            print(token)
