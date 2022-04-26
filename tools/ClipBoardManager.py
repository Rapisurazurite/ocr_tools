import win32clipboard
import win32con
from PIL import ImageGrab
from io import BytesIO


class ClipBoardManager:
    @staticmethod
    def set_clipboard(text: str):
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, text)
        win32clipboard.CloseClipboard()

    @staticmethod
    def get_text_from_clipboard() -> str:
        win32clipboard.OpenClipboard()
        try:
            text = win32clipboard.GetClipboardData(win32con.CF_TEXT)
        except TypeError:
            print("Specified clipboard format is not available")
            return ""
        win32clipboard.CloseClipboard()
        try:
            return text.decode("gbk")
        except UnicodeDecodeError:
            return text.decode("utf-8")

    @staticmethod
    def get_image_from_clipboard() -> BytesIO:
        """
        从剪贴饭返回图片IO流
        :return:
        """
        image = ImageGrab.grabclipboard()
        if image is None:
            raise Exception("未能从剪贴板中读取到图片")
        b = BytesIO()
        image.save(b, 'PNG')
        return b


class QtClipboardManager:
    def __init__(self, cb):
        self.cb = cb

    def get_text_from_clipboard(self):
        if not self.cb.mimeData().hasText():
            return
        text = self.cb.mimeData().text()
        return text

    def get_image_from_clipboard(self):
        if not self.cb.mimeData().hasImage():
            return
        image = self.cb.image()
        image.save('./temp.png')
        return image
