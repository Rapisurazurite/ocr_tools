from unittest import TestCase
from tools import Translator


class TestTranslator(TestCase):

    def test_translate_using_google(self):
        print(Translator.translate_using_google("你好"))
        print(Translator.translate_using_google("Hello"))
        # self.fail()

    def test_translate_using_youdao(self):
        self.fail()
