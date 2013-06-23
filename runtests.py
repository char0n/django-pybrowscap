import sys
from subprocess import call


def runtests():
    call("./runtests.sh")
    sys.exit(0)


if __name__ == '__main__':
    runtests()