import time
import pyautogui
from TextToSpeech import TextToSpeech
from comman_variables import *
from AppOpener import *
from pynput.keyboard import Controller, Key
import pydirectinput
import pygetwindow as gw
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import math
import pyperclip
import win32gui
import cv2

extensions = { "python": ".py", "javascript": ".js", "java": ".java", "c++": ".cpp", "c": ".c", "ruby": ".rb", "swift": ".swift", "kotlin": ".kt", "go": ".go", "rust": ".rs", "typescript": ".ts", "php": ".php", "html": ".html", "css": ".css"}

MediaViewers = ["telegram", "media viewer"]

def Pause_Play():

    #define a controller
    c = Controller()

    #get window names 
    #1st is the site/artist for spotify 
    #2nd is app/song for spotify
    try:
        win = gw.getActiveWindow().title.split('-')
        if len(win) >= 2:
            site = win[len(win) - 2].lower()
            if "youtube" in site:     # for youtube site
                c.press("k")
            elif any(commands in site for commands in MediaViewers):    # for other media players
                c.press(Key.space)
            else:
                c.press(Key.media_play_pause)
        else:   # for other stuff like spotify
            site = win[len(win) - 1].lower()
            if any(commands in site for commands in MediaViewers):  # for other media players
                c.press(Key.space)
            else:   # for other stuff like spotify
                c.press(Key.media_play_pause)
    except:
        # for other stuff like spotify
        c.press(Key.media_play_pause)

def GetVolume():

    # Get default audio device using PyCAW
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    # Get current volume 
    currentVolume = round(volume.GetMasterVolumeLevelScalar()*100)
    # NOTE: -6.0 dB = half volume !

    return currentVolume

def Next_Media():
    c = Controller()
    c.press(Key.media_next)

def Previous_Media():
    c = Controller()
    c.press(Key.media_previous)

def ChangeVolume(Amt = 1,Increment = True):
    # Get default audio device using PyCAW
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    # set current volume 
    currentVolume = volume.GetMasterVolumeLevelScalar()*100
    UpdatedVolume = currentVolume

    if Increment == True:
        # Increase volume by
        amt = Amt # increment by Amt
        if(currentVolume + amt <= 100 and currentVolume + amt >= 0):
            UpdatedVolume = currentVolume + amt
        elif amt > 0:
            UpdatedVolume = 100
        elif amt < 0:
            UpdatedVolume = 0
        
    else:
        # Set Volume to
        amt = Amt
        if(amt <= 100 and amt >= 0):
            UpdatedVolume = amt
        elif amt > 100:
            UpdatedVolume = 100
        elif amt < 0:
            UpdatedVolume = 0
    
    volume.SetMasterVolumeLevelScalar(UpdatedVolume/100, None)

def MuteVolume():
    c = Controller()
    c.press(Key.media_volume_mute)

def Open(software):
    openApp(software, match_closest=True)

def Close(software):
    closeApp(software, match_closest=True)

def GetSentenceAfterWord(text, Word):
    return text.split(Word, 1)[1]

def ConvertMathToReadable(msg): #converts math functions to text

    msg = msg.replace("\\","")
    msg = msg.replace("^", " to the power of ")
    msg = msg.replace("$","")    
    msg = msg.replace("}","{")
    msg = msg.replace("-"," minus ")
    msg = msg.replace("+", " plus ")

    #print(msg)

    lst = []

    if("frac" in msg):
        lst = msg.split("{")
    count = 3
    msg = ""
    
    for item in lst:
        if(count == 1):
            msg = msg + " upon " + item
            count = 3
        elif(count == 2):
            msg = msg + item
            count = 1
        elif(str(item).endswith("frac")):
            msg = msg + item.replace("frac"," ")
            count = 2
        else:
            msg = msg + item
    return msg

def ConvertMsgToCode(msg):
    '''
    the text return has some text and the code with ``` seperating the code from text
    the first line has the program language and rest the code
    '''

    lines = msg.split("```")

    for i in lines:
        if any(line.lower() in i.lower() for line in extensions.keys()):
            code = i.split("\n",1)
            ext = extensions[code[0].split(" ")[0].lower()]
            return code[1], ext
    
    return None, None

    '''
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

def CreateFile(text,filename,extenton,edit = False):

    # check if file name exists and the command is not to edit (edit is false) (create new file)
    if filename in str(file_name_used.keys()).split(".")[0] and edit == False:
        if extenton in str(file_name_used.keys()).split(".")[1]:
            filename = filename + str(file_name_used[filename + "." + extenton]) # change name if it exists
    
    # create file
    f = open(f"F:\python\JARVIS\created files\{filename}.{extenton}", "a+")

    f.seek(0) # go to start of file

    if edit == False: # edit is false i.e to create a new file (remove old text)  
        f.truncate() # delete the text inside the file
    
    elif f.readline() != "": # otherwise edit it and and text without deleting the previous text in file
        f.write("\n \n") # add new line

    f.write(text)

    f.close()

def CopySelectedText():
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(.01)

    return pyperclip.paste()

def PlaySpotifyMusic(MusicName):# get only one window

    global Spotify
    
    msg = f"Playing {MusicName} On Spotify"
    print(msg)
    TextToSpeech(msg)

    if Spotify == None:
        openApp("Spotify", match_closest = True)
        time.sleep(2)
    else:
        openApp("Spotify", match_closest = True)
    
    time.sleep(.2)
    Spotify = gw.getActiveWindow()

    # Get Original Dimensions
    left = Spotify.left
    top = Spotify.top
    width = Spotify.width
    height = Spotify.height

    print(Spotify)

    Spotify.left = (-10000) # Hide It From View

    time.sleep(1)
    # Open Quick Search And Search For song and play it
    pyautogui.hotkey('ctrl','k') # Open Quick Search
    pyautogui.write(MusicName) # Search For song
    time.sleep(1)
    pyautogui.press('Enter') # play it
    time.sleep(.2)
    
    #setWindowDimension(Spotify) # Reset Its Dimensions To Default Setting
    setWindowDimension(Spotify, left, top, height, width) # Reset Its Dimensions To Original
    Spotify.minimize()

def GetMusicName():
    Title = Artist = None
    if Spotify != None:
        # Get Spotify Music Name
        if '-' in Spotify.title.lower():
            print(Spotify.title)
            Title = Spotify.title.split('-')[1].strip()
            Artist = Spotify.title.split('-')[0].strip()

    '''TODO Gives Result even if the video is not playing not what we want'''
    '''
    elif gw.getWindowsWithTitle("YouTube") != []:
        # Get Youtube Video Name 
        win_title = gw.getWindowsWithTitle("YouTube")[0].title.split('-')[0].strip()
        if win_title != 'YouTube':
            Title = win_title
    '''

    return Title,Artist
    
def setWindowDimension(window, left = 400, top = 100, height = 1110,width = 2017):
    window.size = (width,height)
    window.left = (left)
    window.top = (top)

def ZoomIn():
    pyautogui.keyDown('ctrl')
    pyautogui.press('=')
    pyautogui.keyUp('ctrl')

def ZoomOut():
    pyautogui.keyDown('ctrl')
    pyautogui.press('-')
    pyautogui.keyUp('ctrl')

def AddObject(obj = ""):
    if "Blender" in gw.getActiveWindow().title:
        pydirectinput.keyDown('shift')
        pydirectinput.press('a')
        pydirectinput.keyUp('shift')

        if obj != "":
            pyautogui.write(obj) # search for obj
            pyautogui.press('enter') # add the obj

def Delete():
    if "Blender" in gw.getActiveWindow().title:
        pyautogui.press('x')
        pyautogui.press('enter')
    else:
        pyautogui.press('del')

def reMap(value, maxInput, minInput, maxOutput, minOutput):

	value = maxInput if value > maxInput else value
	value = minInput if value < minInput else value

	inputSpan = maxInput - minInput
	outputSpan = maxOutput - minOutput

	scaledThrust = float(value - minInput) / float(inputSpan)

	return minOutput + (scaledThrust * outputSpan)

''' run code of diffrent file'''
# f = open("CheckCommands.py")
# exec(f.read())

'''
from win32 import win32clipboard
win32clipboard.OpenClipboard()
win32clipboard.EmptyClipboard()
win32clipboard.CloseClipboard()
'''

