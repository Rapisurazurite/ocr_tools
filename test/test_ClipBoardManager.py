from unittest import TestCase
from PIL import Image

from tools import ClipBoardManager as cbm
import os


class TestClipBoardManager(TestCase):
    def test_get_text_from_clipboard(self):
        text = "abcdabcd"
        cbm.set_clipboard(text)
        print("SET CLIPBOARD TO '{}'".format(text))
        return cbm.get_text_from_clipboard() == text

    def test_get_image_from_clipboard(self):
        file_name = "save.png"
        b = cbm.get_image_from_clipboard()
        img = Image.open(b)
        img.save(file_name, "png")
        if os.path.isfile(file_name):
            # os.remove("asd.png")
            pass
        else:
            TestCase.fail()
