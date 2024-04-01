import os
import pygetwindow as gw

# assigning name
Ai_Name = "jarvis"

# User name and image
user_photo = None
previous_user_name = ''
user_name = ''

# Face Detection
CreateUser = False
FaceDetectInterval = 5   # when counter reaches this it detects face
FaceDetectedSince = 5 # counter for when to detect face

# Text To Speech
isSpeaking = False
speach = "" # The Threading Obj Which is responsible for starting and stoping the text to speach

# Var to Check If Name Was Called
NameCalled = False

# generated images
Images = ["https://tse2.mm.bing.net/th/id/OIG.gM8YPvF0wj2aYDaDzi_K",
"https://tse3.mm.bing.net/th/id/OIG.Y1AVIoQ63cVQEUPTDrhL",
"https://tse4.mm.bing.net/th/id/OIG.VW8JoadAk7xWKwIy3oDQ",
"https://tse3.mm.bing.net/th/id/OIG.nLNPTI63ubceZVuSaW6L"]
Image_Window_Open = False
Image_No = 0

# Command Processing
Processing_Command = False

# Windows
Windows = gw.getAllTitles()
ActiveWindow = gw.getActiveWindow()

def getSpotifyWindow():
    spotify = gw.getWindowsWithTitle("Spotify Free") # returns list of window

    # get only one window
    if spotify != []:  
        spotify = spotify.pop()
    else:
        spotify = None

    return spotify

Spotify = getSpotifyWindow()

# Type text
StartedTyping = False

# Created Files
path = 'F:\python\JARVIS\created files'
file_name_used = {}

# assign a dic to all used file names and the number which should be added at end to avoid duplcates
for file in os.listdir(path):
    try:
        file = file.split(".")
        if str(file[0])[-1].isalpha():
            file_name_used[file[0] + "." + file[1]] = "0" # assigns 0 as for if there is a same name file you can change name to 0
        else:
            file_name_used[file[0][:-1] + "." + file[1]] = int(str(file[0])[-1]) + 1 # assigns next number to put if you have same name

    except Exception as e:
        #print(e)
        pass
