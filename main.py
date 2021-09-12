import sys

from dism import DISM

if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("Usage: main.py [script]")
        sys.exit()

    DISM().run(open(sys.argv[1]).read())
