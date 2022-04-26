import ctypes
import sys
import os

curPath = os.path.split(__file__)[0]
curPath = os.path.split(curPath)[0]
dll = ctypes.cdll.LoadLibrary(os.path.join(curPath, "TXGYMailCamera.dll"))


def capture():
    return dll.CameraWindow(0)


if __name__ == "__main__":
    capture()
