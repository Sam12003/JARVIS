import time
import pyautogui

time.sleep(2)

print("hi")
pyautogui.keyDown('ctrl')
pyautogui.press('=')
pyautogui.keyUp('ctrl')