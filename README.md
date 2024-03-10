# JARVIS: AN AI ASSISTANT FOR WINDOWS
it uses bing copiot to help you with you questions and it also works offline for task related to you pc like opening app, playing music, text to speach, voice to text,etc

# SETUP
1. in Jarvis\face_detection_v1 add a new file named "faces" this will store a database of all reconised faces for face recogition add images with the name of photo as the name of the person, The AI also does this automatically if the person is not recognised
2. create a text file "BING_COOKIES.txt" in the Jarvis File and enter you bing cookies in it (optional)

# THINGS JARVIS CAN DO:
1. You can change The Name Of AI: in "comman_variables.py" Change "Ai_Name" to the name of the assistant you want

## Some Commands Require You To Say The AI Name before saying command
> Once You Say The AI name it will Process everything you say and if you want it to stop listening just say one of these commands ["goodbye", "good bye", "bye" "talk to you later"]

### EXAMPLES OF SUCH COMMANDS:
1. say Hello to greet the ai
2. say "Write {the code you want it to write} in {coding language of your choice} To Ask the Ai to write a code in any language {requires internet}
3. Tell it a math problem and it will solve it  *
4. if you say any thing else it will ask BING COPILOT for the answer and tell you what it says

## COMMANDS WHICH DON'T REQUIRE YOU TO SAY AI NAME:
1. Say one of these ["type","start typing"] to Start Voice To Text
2. Say one of these ["stop","stop typing","stop writting","stop listening"] to Stop Voice To Text
3. Say "Open" or "Close" along with the app name to open/close that app
4. Say "Pause" or"Stop" to stop the music/media that is playing
5. Say one of these ["play","continue","resume"] to Stop Music/Media that is playing
6. if you add a music name to the above command it will open spotify and play that music in the background {requires Spotify Desktop APP}
7. Say one of these ["turn up volume","volume up","increase sound","increase volume","turn up sound"] to increase volume 
* can also tell it to increase to {the percentage of volume eg) increase volume to 50 }
* can also tell it to increase by {the percentage of volume eg) increase volume by 10 }
8. Say one of these ["turn down volume","volume down","lower sound","lower volume","increase sound","increase volume","turn down sound"] to decrease volume
* can also tell it to decrease to {the percentage of volume eg) decrease volume by 50 }
* can also tell it to decrease by {the percentage of volume eg) decrease volume by 10 }
9. tell it to "mute" to mute/unmute volume
10. say "next" to play next song/media
11. say "previous" to play previous song/media
12. say ["what music is this", "what song", "song name", "song playing","which song","music name"] to get music name that is playing
13. say one of these ["read", "say","text on screen"] to read the selected text {also copies it to clipboard}
14.  it takes a photo of your face and does a face recognition on it to know the user name {requires camera}
15. say your name if it says "Sorry I Dont Know You! Can You Tell Me Your Name" , it will automatically save the photo with your name in the faces folder

## Create More Commands/Ways To Say it
1. go to "CheckCommands.py" and there you will find a lot of list which you can change/add ways to call a specific command
2. in "Commands.py" you will see all the commands

* it uses bing copilot AI to answer some of the questions
