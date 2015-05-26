import sys
from eitleain import Eitleain


def main():
    eitleain = Eitleain()
    for aircraft in eitleain.watch():
        print(aircraft)
    return True


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
