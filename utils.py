import base64
import json
from typing import Tuple

import requests
import win32con
import win32gui

from tools import Translator


class Window:  # 剪切板监听
    def __init__(self):
        # 注册一个窗口类
        wc = win32gui.WNDCLASS()
        wc.lpszClassName = 'MyWindow'
        wc.hbrBackground = win32con.COLOR_BTNFACE + 1
        wc.lpfnWndProc = self.wndProc
        class_atom = win32gui.RegisterClass(wc)
        # 创建窗口
        self.hwnd = win32gui.CreateWindow(class_atom, u'OCR',
                                          win32con.WS_OVERLAPPEDWINDOW,
                                          win32con.CW_USEDEFAULT,
                                          win32con.CW_USEDEFAULT,
                                          win32con.CW_USEDEFAULT,
                                          win32con.CW_USEDEFAULT, 0, 0, 0, None)

    # 消息处理
    def wndProc(self, hwnd, msg, wParam, lParam):
        if msg == win32con.WM_DESTROY:
            win32gui.PostQuitMessage(0)
        if msg == win32con.WM_DRAWCLIPBOARD:  # 当剪切板更新的时候收到这个消息
            self.call_function()
            return win32gui.DefWindowProc(hwnd, msg, wParam, lParam)

    def call_function(self):
        pass


class MyWindow(Window):
    def call_function(self):
        pass










if __name__ == '__main__':
    a = """For abstract could
the readers to read even purchase your pap"""
    b = Translator.translate_using_youdao(a)
    print(b)
