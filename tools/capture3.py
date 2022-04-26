import ctypes
import sys
import os

curPath = os.path.split(__file__)[0]
curPath = os.path.split(curPath)[0]
exe = os.path.join(curPath, "NiuniuCapture.exe")


def capture():
    return os.system("{} niuniu,'',0,0,0,0,0,0".format(exe))


if __name__ == "__main__":
    capture()
