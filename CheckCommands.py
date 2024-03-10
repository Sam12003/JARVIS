import asyncio
import comman_variables as Jarvis
from TextToSpeech import TextToSpeech
from Commands import *
from ChatBot import *
import cv2

#   ways to say commands
Goodbye = ["goodbye", "good bye", "bye" "talk to you later"]
Generate = ["create", "generate", "produce"]
Math = ["+", "equals", "-","subtract","add", "sum","diffrence","divide","tan","cos","cot","sec","cosec","sin","dx","integrate","diffrenciate"]
Write = ["write"]
Program = ["program", "code"]
extensions = { "Python": ".py", "JavaScript": ".js", "Java": ".java", "C++": ".cpp", "C": ".c", "Ruby": ".rb", "Swift": ".swift", "Kotlin": ".kt", "Go": ".go", "Rust": ".rs", "TypeScript": ".ts", "PHP": ".php", "HTML": ".html", "CSS": ".css"}
Pause = ["pause","stop"]
Play = ["play","continue","resume"]
Volumeup = ["turn up volume","volume up","increase sound","increase volume","turn up sound"]
Volumedown = ["turn down volume","volume down","lower sound","lower volume","increase sound","increase volume","turn down sound"]
StartTyping = ["type","start typing"]
StopTyping = ["stop","stop typing","stop writting","stop listening"]
GetMusic = ["what music is this", "what song", "song name", "song playing","which song","music name"]
GetTextOnScreen = ["read", "say","text on screen"]

print(Jarvis.Ai_Name)
def CheckCommand(text):

    # Save Photo With Name Of New User
    if Jarvis.CreateUser == True:
        print("updating")
        if 'name is' in text.lower():
            name = text.lower().split('name is')[1].capitalize()
        else:
            name = text.capitalize()
            print(f"your name is {name}")
        
        Jarvis.user_name = name
        target_file_name = fr'F:\python\JARVIS\face_detection_v1\faces\{name}.jpg'

        cv2.imwrite(
            target_file_name,
            Jarvis.user_photo,
        )
        
        return

    count = 0
    hi = False

    if any(commands in text.lower() for commands in StartTyping):
        Jarvis.StartedTyping = True

    if(Jarvis.StartedTyping == True):
        if any(commands in text.lower() for commands in StopTyping):
            Jarvis.StartedTyping = False
            TextToSpeech("typing has been stoped")
            return

        # Get Words Without Instruction
        resultwords  = [word for word in text.split() if word.lower() not in StartTyping]
        result = ' '.join(resultwords)

        pyautogui.typewrite(result)
        return
    
    if any(commands in text.lower() for commands in GetTextOnScreen):
        # Get The Text Which Is Highlighted And Read It

        msg = CopySelectedText()

        print(msg)
        TextToSpeech(msg)

    if "open" in text.lower():
        app_name = GetSentenceAfterWord(text, "open").split()[0]
        msg = "opening " + app_name
        print(msg)
        TextToSpeech(msg)
        Open(app_name)
        count = count + 1
        Jarvis.Images = []

    if "close" in text.lower():
        if Jarvis.Image_Window_Open == True:
            msg = "closeing image"
            print(msg)
            TextToSpeech(msg)
            CloseImage()
            count = count + 1
        else:
            app_name = GetSentenceAfterWord(text, "close").split()[0]
            msg = "closeing " + app_name
            print(msg)
            TextToSpeech(msg)
            Close(app_name)
            count = count + 1
            Jarvis.Images = []

    if any(commands in text.lower() for commands in Pause) or "old song" == text.lower() or "top song" == text.lower():
        msg = "Pausing"
        print(msg)
        TextToSpeech(msg)
        Pause_Play()
        count = count + 1
        Jarvis.Images = []

    if any(commands in text.lower() for commands in Play):

        if('play' in text.lower()):
            try:
                MusicName = text.lower().split('play')[1].strip().replace('on spotify','').strip() # check if the commands wants to play music from spotify
                if(MusicName != ''):
                    PlaySpotifyMusic(MusicName)
                    count = count + 1
                    return
            except:
                pass # Or Only play the curent media beign played

        msg = "Playing"
        print(msg)
        TextToSpeech(msg)
        Pause_Play()
        count = count + 1
        Jarvis.Images = []

    if "volume" in text.lower() or "sound" in text.lower() or "mute" in text.lower():

        if "mute" in text.lower():
            MuteVolume()

        elif "to" in text.lower():
                for x in text.split():
                    if x.isnumeric():
                        amt = int(x)
                        ChangeVolume(amt, False)    
                        msg = f"volume changed to: {GetVolume()}%"    

        elif any(commands in text.lower() for commands in Volumeup):
            if "by":
                for x in text:
                    if x.isnumeric():
                        amt = int(x)
                        ChangeVolume(amt, True)
                        msg = f"volume increased by: {amt}% , current volume is {GetVolume()}%"
            else:
                ChangeVolume()
                msg = f"volume changed to: {GetVolume()}%"

        elif any(commands in text.lower() for commands in Volumedown):  
            if "by":
                for x in text:
                    if x.isnumeric():
                        amt = -x
                        ChangeVolume(amt, True)
                        msg = f"volume decreased by: {amt}% , current volume is {GetVolume()}%"
            else:
                ChangeVolume(-1)
                msg = f"volume changed to: {GetVolume()}%"
        
        else:
            msg = f"Current Volume is: {GetVolume()}%"

        print(msg)
        TextToSpeech(msg)     
          
    if "next" in text.lower():
        if Jarvis.Image_Window_Open == True:
            if  Jarvis.Image_No < 4:
                imageNO = Jarvis.Image_No + 1
            else:
                imageNO = 0

            #show images
            url = str(Jarvis.Images[imageNO])
            window_name = "Generated Image"
            threading.Thread(target = ShowImage, args = (url, window_name) ).start()

            msg = "showing next image"

            count = count+1
            print(msg)
            TextToSpeech(msg)
            #close window by pressing any key
        
        else:
            Next_Media()

    if "previous" in text.lower():
        Previous_Media()
    
    if any(commands in text.lower() for commands in GetMusic):
        Title,Artist = GetMusicName()
        if Title != None and Artist != None:
            msg = f"{Title} by {Artist}"
            print(f"{'':-^50} \nTitle: {Title}\nArtist: {Artist} \n{'':-^50}")
        elif Title != None:
            msg = f"{Title} by {Artist}"
            print(f"{'':-^50} \nTitle: {Title}\n{'':-^50}")
        else:
            msg = "Sorry Could Not Hear Any Music"
            print(msg)

        TextToSpeech(msg)

    if(Jarvis.Ai_Name in text.lower() or Jarvis.NameCalled == True):
        
        print(Ai_Name + ": ", end="", flush=True)

        if "hello" in text.lower():
            msg = "Hello! How can I help you?"
            print(msg)
            TextToSpeech(msg)
            print()
            count = count + 1
            Jarvis.Images = []
            hi = True

        if any(commands in text.lower() for commands in Write):
            if any(commands in text.lower() for commands in Program):
                if any(language.lower() in text.lower() for language in extensions.keys()):
                    style = "precise"
                    msg = asyncio.run(AiResponceStyle(text, style))

                    code = ConvertMsgToCode(msg)
                    print(code)
                    count += 1

        if any(command in text.lower() for command in Generate):
            if("image" in text.lower()):
                Jarvis.Images = CreateImages(text)
                if Jarvis.Images != None:
                    print("Images Created.")
                    TextToSpeech("Images Created")
                    print(Jarvis.Images)
                    for img in Jarvis.Images:
                        if not str(img).endswith(".svg"):
                            print(img)
                    count = count + 1

                    #show images
                    url = str(Jarvis.Images[0])
                    window_name = "Generated Image"
                    threading.Thread(target = ShowImage, args = (url, window_name) ).start()
    
                    #close window by pressing any key


                if Jarvis.Images != None or Jarvis.Images != []:
                   #save images
                   SavedImage = SaveImages(Jarvis.Images)
                   print(str(SaveImages) + " images saved") # no of images saved
                   count = count + 1

        if any(command in text.lower() for command in Goodbye) and hi == False:
            msg = "Goodbye! Just Say " + str(Jarvis.Ai_Name) + " if you need any help!" #stop listening if you say goodbye
            print(msg)
            TextToSpeech(msg)

            NameCalled = False
            count = count + 1
            Jarvis.Images = []

            return True

        if any(command in text.lower() for command in Math): #math functions
    
            count = count + 1
            Jarvis.Images = []

            style = "precise"
            asyncio.run(AiResponceStyle(text, style))
            msg = str(msg)

            msg = ConvertMathToReadable(msg)

            if msg != None:
                print(msg) #there was a response
                TextToSpeech(msg) #error
            else:
                msg = "Sorry Something Went Wrong" #no response there was an error
                print(msg)
                TextToSpeech(msg)

        if(count == 0):
            msg = asyncio.run(AiResponce(text))  #give creative answers
            Jarvis.Images = []
            if msg != None:
                print(msg) #there was a response
                TextToSpeech(msg) #error
            else:
                msg = "Sorry Something Went Wrong" #no response there was an error
                print(msg)
                TextToSpeech(msg)


