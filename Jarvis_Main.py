import speech_recognition as sr
from comman_variables import *
from TextToSpeech import TextToSpeech
from CheckCommands import *
import comman_variables as Jarvis
import threading
import pyaudio
from face_detection_v1.DetectFaces import *

# Create an instance of the Recognizer class:
recognizer = sr.Recognizer() 

# Create a function to capture voice input from the user using a microphone:
def capture_voice_input():
    global Ai_Name,NameCalled
    print(Ai_Name + ": ", end="", flush=True)
    '''try:
        with sr.Microphone(2) as source: #for headset but lowers sound quality
            msg = "Listening..." 
            print(msg)
            audio = recognizer.listen(source)
        return audio
    except:'''
    with sr.Microphone() as source:
        msg = "Listening..." 
        print(msg)
        audio = recognizer.listen(source)
    return audio


# Create a function to convert the captured voice input to text:
def convert_voice_to_text(audio):
    global Ai_Name,NameCalled
    try:
        text = recognizer.recognize_google(audio)
        msg = "You said: " + text
        print(msg)
        
    except sr.UnknownValueError:
        text = ""
        if(NameCalled == True):
            msg = "Sorry, I didn't understand that."
            print(msg)
        
    except sr.RequestError as e:
        text = ""
        print("Error; {0}".format(e))

    return text

# Create a function to process the voice commands:
def process_voice_command(text):
    global Ai_Name,NameCalled
    arg1 = text
    CheckCommand(arg1)

    return False

# calling spotify features
def StopAdsSpotifycall():
    import Spotify.stopSpotifyAd 

# initialize stop ads spotify program
#threading.Thread(target = StopAdsSpotifycall).start()

def DetectFace():

    try:
        Jarvis.previous_user_name = Jarvis.user_name
        Jarvis.user_photo,Jarvis.user_name,_,_ = Detect_Face()
        print(f"user: {Jarvis.user_name}")

    except Exception as e:
        print(f'--------{e}--------')

# Create a main function to run the voice recognition system:
def main():

    # Encode Known Faces   
    encode_face()

    # voice recognition
    end_program = False

    while not end_program:
        
        # all global variables
        global CheckNewFace,FaceDetectInterval,FaceDetectedSince,CreateUser

        # detect face from camera

        if FaceDetectedSince >= FaceDetectInterval:
            DetectFace()
            FaceDetectedSince = 0
    
        FaceDetectedSince += 1

        Jarvis.CreateUser = False

        # user not defined (no saved photo of user)        
        if Jarvis.user_name == 'Unknown':
            # Create the user
            msg = "Sorry I Dont Know You! Can You Tell Me Your Name"
            
            print(msg)
            TextToSpeech(msg)

            Jarvis.CreateUser = True

        # CHECK IF USER CHANGED
        elif Jarvis.user_name != '':
            if(Jarvis.user_name != Jarvis.previous_user_name):
                # greet new user
                msg = f"Hello {Jarvis.user_name}! How Can I Help You"
                print(msg)
                TextToSpeech(msg)

                # change previous user to new user
                Jarvis.previous_user_name = Jarvis.user_name

        # VOICE RECOGNITION
        audio = capture_voice_input()
        text = convert_voice_to_text(audio)
        end_program = process_voice_command(text)

        if Jarvis.CreateUser == True:
            encode_face()
            Jarvis.CreateUser = False
if __name__ == "__main__":
    main()
