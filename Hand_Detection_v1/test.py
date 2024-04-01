import time
import pyautogui
import pydirectinput
import pygetwindow as gw

#time.sleep(2)

print("hi")

# pyautogui.keyDown('ctrl')
# pyautogui.press('=')
# pyautogui.keyUp('ctrl')

# pyautogui.moveTo(1,1)

#pydirectinput.keyDown('shift')
#pydirectinput.mouseDown(button='middle')
#print("hi")

#pyautogui.moveTo(2048.0, 1440.0)

# pyautogui.press('x')
# pyautogui.press('enter')

import pyttsx3
import multiprocessing
import time

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    # Start speaking
    p = multiprocessing.Process(target=speak, args=("Hello, I am speaking this sentence.",))
    p.start()

    # Stop speaking after 2 seconds
    time.sleep(2)
    print("hi")
    p.terminate()
    p = multiprocessing.Process(target=speak, args=("Hello, I am speaking this sentence.",))
    p.start()