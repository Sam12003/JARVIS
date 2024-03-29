import time
import pyautogui
import pydirectinput

time.sleep(2)

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

def Compute(A,B,C="*"):
    for i in range(A,B+1):
        if i % 2 == 0:
            print(i,C)
        else:
            print(i,"@")
    print()

Compute(10,14)
Compute(25,29,"#")
Compute(5,10)
        