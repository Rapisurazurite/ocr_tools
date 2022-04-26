import keyboard
import os

class LaTexHelper:
    @staticmethod
    def add_abbreviation():
        curPath = os.path.split(__file__)[0]
        curPath = os.path.split(curPath)[0]
        csv = os.path.join(curPath, "replace_table.csv")
        with open(csv) as f:
            replacements = f.readlines()
        for each_line in replacements:
            options = each_line.replace(" ", "").split(",")
            options = [x.replace("'", "") for x in options]
            keyboard.add_abbreviation(options[0], options[1], match_suffix=True)