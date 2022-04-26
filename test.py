from utils import LaTexHelper
import keyboard


def func():
    print("Start record")
    recorded = keyboard.record(until=" ")
    print(recorded)


if __name__ == "__main__":
    recorded = keyboard.record(until=' ')
    # 当按下esc时结束按键监听，并输出所有按键事件
    print(recorded)
    keyboard.add_abbreviation('\\', func)
    keyboard.wait()
