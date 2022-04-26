import sys
from io import BytesIO
import keyboard
from PyQt5.QtWidgets import QApplication

from tools import ClipBoardManager, LaTexHelper, Matpix_MyAccount, Bing_LaTex_OCR, BaiduOCR, BaiduHandWritingOCR
from tools import SimpleScreenShot

# this specifies the ocr engine
OcrSwitch = 0


def save_screenshot() -> BytesIO:
    """
    保存截图到BytesIO.
    Currently use QT to get the screenshot
    available:
        1. QT
        2. Wechat Screenshot Api
        3. NiuNiu Screenshot Api
    Because API cannot support high resolution and multi-window,
    so we use QT to get the screenshot.
    :return: BytesIO
    """
    app = QApplication(sys.argv)
    window = SimpleScreenShot()
    window.simple_screen_shot()
    app.exec_()
    img = window.img
    return BytesIO(img)


def callback_baidu():
    """
    使用百度OCR识别图片，主要OCR的是文字
    :return:
    """
    try:
        b = save_screenshot()
        # 进行百度识图
        result = BaiduOCR().ocr(b)
        # 将空格去除
        result = result.replace(' ', '')
        print(result)
        ClipBoardManager.set_clipboard(result)
    except AttributeError:
        print('[INFO]未读取到剪贴板信息')
    except Exception as e:
        print(e)


def callback_matpix():
    """
    使用matpix(Bing)的OCR识别图片，主要OCR的是公式
    :return:
    """
    print('[INFO]正在识别图片')
    try:
        b = save_screenshot()
        # 判断b是否为空
        if b is None:
            print('[INFO]未读取到剪贴板信息')
            return
        # 使用公式识别的API设置
        if OcrSwitch == 2:
            success, result = Matpix_MyAccount.ocr(b)
        elif OcrSwitch == 3:
            success, result = Bing_LaTex_OCR.ocr(b)
        elif OcrSwitch == 4:
            success = True
            result = BaiduHandWritingOCR().ocr(b)
        else:
            print("[ERROR] No Correct Choice")
            sys.exit(0)

        print(result)
        if success:
            ClipBoardManager.set_clipboard(result)
    except AttributeError:
        print('[INFO]未读取到剪贴板信息')
    except Exception as e:
        print('[ERROR]', e)
    print('[INFO]识别完成, 已复制到剪贴板')


if __name__ == '__main__':
    print("选择你所需要使用的OCR引擎:",
          "2. Mathpix_MyAccout",
          "3. Bing (Free)",
          "4. Baidu HandWriting")
    OcrSwitch = int(input())
    print("***Start***")
    keyboard.add_hotkey('alt+q', callback_matpix)
    keyboard.add_hotkey('alt+z', callback_baidu)

    # Latex 快捷替换功能
    # 将这一行注释掉，可以关闭LaTex快捷替换功能
    LaTexHelper.add_abbreviation()
    keyboard.wait()