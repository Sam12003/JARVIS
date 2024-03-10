import asyncio
import comman_variables as Jarvis
import cv2
import time
import requests
import threading
from pywinauto import findwindows
import win32gui
from functools import lru_cache

# Import the package
from BingImageCreator import ImageGen
from sydney import SydneyClient
import urllib.request 
from PIL import Image 
import pyautogui

msg = ""

async def AiResponce(prompt):
    async with SydneyClient() as sydney:
        global msg

        try:
            msg = await sydney.ask(prompt)
            return msg
        except Exception as e:
            print("--------" )
            print(e)
            if "ConversationLimitException" in str(e):
                Reset()
                return None
            else:
                print("sry but something went wrong")
                return None
        
async def AiResponceStyle(prompt,style):
    async with SydneyClient(style = style) as sydney:

        global msg

        try:
            msg = await sydney.ask(prompt)
            return msg
        except Exception as e:
            print("--------" )
            print(e)
            if "ConversationLimitException" in str(e):
                Reset()
                return None
            else:
                print("sry but something went wrong")
                return None

async def Reset():
    async with SydneyClient() as sydney:
        await sydney.reset_conversation()

def CreateImages(prompt):
    #get cookies
    f = open("BING COOKIES.txt", "r")
    data = f.read()
    f.close()

    # Create an image generator object with the cookie
    image_generator = ImageGen(auth_cookie=data, auth_cookie_SRCHHPGUSR=data)

    # Generate images for a prompt
    try:
        Images = image_generator.get_images(prompt = prompt)
        return Images
    except Exception as e:
        print(e)
        return None

def SaveImages(images, name = "image", path = "F:\python\JARVIS\Generated Images\\" ):
    count = 0
    imagename = name
    for image in images:
        try:
            time.sleep(2)
            print("Saving IMG")
            session = requests.Session()
            session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.1.2222.33 Safari/537.36",
            "Accept-Encoding": "*",
            "Connection": "keep-alive"
            }
            response = session.get(image)
            print("------------- " + path)
            f = open(path + "\\" + imagename + str(count) +".png", "wb")
            f.write(response.content)
            print(f)
            count = count + 1
        except Exception as e:
            print(e)
    return str(count)

def ShowImage(url,window_name = "Generated Image"):
    images = [url]
    count = SaveImages(images, "GeneratedImage","F:\python\JARVIS")
    if(count == "1"):
        
        # set the window to be active
        hWnd = win32gui.FindWindow(None, window_name)
        if(hWnd != 0):  #check if window exits
            win32gui.SetForegroundWindow(hWnd)

        CloseImage()
        
        #window name
        window_name = window_name

        # Reading an image in default mode 
        image = cv2.imread("GeneratedImage0.png") 
  
        # Naming a window 
        cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE) 
  
        # Using moveWindow() to get it to centre
        cv2.moveWindow(window_name, 900, 100)  

  
        # Displaying the image 
        cv2.imshow(window_name, image)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1) 

        # set the window to be active
        hWnd = win32gui.FindWindow(None, window_name)
        win32gui.SetForegroundWindow(hWnd)

        Jarvis.Image_Window_Open = True

        # waits for user to press any key 
        # (this is necessary to avoid Python kernel form crashing) 
        cv2.waitKey()
        cv2.destroyAllWindows()
    else:
        Jarvis.Image_Window_Open = False
        
    return None

def CloseImage():
    pyautogui.press("left")

#--------------------- Threading example ---------------------
'''
does the process in background

arg1 = "https://tse2.mm.bing.net/th/id/OIG.qkqVB3abUurbT4Iv2eJs"
arg2 = "Generated Image"
threading.Thread(target = ShowImage, args = (arg1, arg2) ).start()

'''

#  --------------------- Get Code ---------------------
'''
the text return has some text and the code with ``` seperating the code from text
the first line has the program language and rest the code

print(asyncio.run(AiResponceStyle("write a cool python program give", "precise")).split("```")[1])

the output you get is:

python
def fibonacci(n):
    sequence = [0, 1]
    while sequence[-1] < n:
        sequence.append(sequence[-1] + sequence[-2])
    return sequence

n = int(input("Enter a number: "))
print(f"Fibonacci sequence up to {n}: {fibonacci(n)}")

'''

#------------------ get active window --------------------
'''
from win32gui import GetWindowText, GetForegroundWindow
print(GetWindowText(GetForegroundWindow()))
'''

