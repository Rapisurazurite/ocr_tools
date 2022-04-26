from unittest import TestCase

import keyboard

from tools import LaTexHelper


class TestLaTexHelper(TestCase):
    def test_add_abbreviation(self):
        LaTexHelper.add_abbreviation()
        keyboard.wait()
