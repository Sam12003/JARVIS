1} in Jarvis\face_detection_v1 add a new file named "faces" this will store a database of all reconised faces for face recogition add images with the name of photo as the name of the person, The AI also does this automatically if the person is not recognised
2} create a text file "BING_COOKIES.txt" in the Jarvis File and enter you bing cookies in it (optional)

# THINGS JARVIS CAN DO:
1} You can change The Name Of AI: in "comman_variables.py" Change "Ai_Name" to the name of the assistant you want

# Some Commands Require You To Say The AI Name before saying command
# Once You Say The AI name it will Process everything you say and if you want it to stop listening just say one of these commands ["goodbye", "good bye", "bye" "talk to you later"]

# EXAMPLES OF SUCH COMMANDS:
* say Hello to greet the ai
* say "Write {the code you want it to write} in {coding language of your choice} To Ask the Ai to write a code in any language *
* Tell it a math problem and it will solve it  *
* if you say any thing else it will ask BING COPILOT for the answer and tell you what it says

# COMMANDS WHICH DON'T REQUIRE YOU TO SAY AI NAME:
* Say one of these ["type","start typing"] to Start Voice To Text
* Say one of these ["stop","stop typing","stop writting","stop listening"] to Stop Voice To Text
* Say "Open" or "Close" along with the app name to open/close that app
* Say "Pause" or"Stop" to stop the music/media that is playing
* Say one of these ["play","continue","resume"] to Stop Music/Media that is playing
* if you add a music name to the above command it will open spotify and play that music in the background * {requires Spotify Desktop APP}
* Say one of these ["turn up volume","volume up","increase sound","increase volume","turn up sound"] to increase volume 
--> can also tell it to increase to {the percentage of volume eg) increase volume to 50 }
--> can also tell it to increase by {the percentage of volume eg) increase volume by 10 }
* Say one of these ["turn down volume","volume down","lower sound","lower volume","increase sound","increase volume","turn down sound"] to decrease volume
--> can also tell it to decrease to {the percentage of volume eg) decrease volume by 50 }
--> can also tell it to decrease by {the percentage of volume eg) decrease volume by 10 }
* tell it to "mute" to mute/unmute volume
* say "next" to play next song/media
* say "previous" to play previous song/media
* say ["what music is this", "what song", "song name", "song playing","which song","music name"] to get music name that is playing
* say one of these ["read", "say","text on screen"] to read the selected text {also copies it to clipboard}
* it takes a photo of your face and does a face recognition on it to know the user name {requires camera}
* say your name if it says "Sorry I Dont Know You! Can You Tell Me Your Name" , it will automatically save the photo with your name in the faces folder

# Create More Commands/Ways To Say it
1} go to "CheckCommands.py" and there you will find a lot of list which you can change/add ways to call a specific command
2} in "Commands.py" you will see all the commands

* {requires internet}
* it uses bing copilot AI to answer some of the questions
