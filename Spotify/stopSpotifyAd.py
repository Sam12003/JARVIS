from AppOpener import *
from pynput.keyboard import Controller, Key
import pyautogui
import time
from spotipy.oauth2 import SpotifyClientCredentials
import pygetwindow as gw
import sys
sys.path.append('F:\python\JARVIS') 
import comman_variables as Jarvis

def StopAdsSpotify():
    while True:
        if(Jarvis.Windows != gw.getAllTitles()):
            print("check")
            for x in gw.getAllTitles():
                if("advertisement" in x.lower()):
                    
                    spotifyopen = False

                    print("AD Detected")
                    Jarvis.ActiveWindow = gw.getActiveWindow()

                    if "advertisement" in Jarvis.ActiveWindow.title.lower():  spotifyopen = True # Active window is not Spotify

                    closeApp("Spotify", match_closest=True)
                    openApp("Spotify", match_closest=True)
    
                    c = Controller()
    
                    time.sleep(1)
    
                    c.press(Key.media_play_pause)
                    c.press(Key.media_next)

                    Jarvis.Spotify = gw.getActiveWindow()
                    
                    if spotifyopen == False:  Jarvis.Spotify.minimize()                                         # hide spotify window

                    try:
                        if Jarvis.ActiveWindow.isMinimized: Jarvis.ActiveWindow.maximize()
                        Jarvis.ActiveWindow.activate()
                    except:
                        pass
                
                elif("spotify free" in x.lower()):
                    Jarvis.Spotify = Jarvis.getSpotifyWindow()

            Jarvis.Windows = gw.getAllTitles()
    
            time.sleep(2)

StopAdsSpotify()