class DismErrors:
    had_error = False

    @staticmethod
    def error(line: int, message: str) -> None:
        DismErrors.report(line, message)

    @staticmethod
    def report(line: int, message: str) -> None:
        print(f"[line {line}] {message}")
        DismErrors.had_error = True
