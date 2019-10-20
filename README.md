# LDR-Controlled-Roll-Along
LDR Controller For Pygame Using An Arduino


Roll Along is a arcade style game created using Pygame. This game is really simple with currently only three components as its basis. The user is a red ball that has to navigate a randomly generated maze to get to the other side of the screen. However smaller blue balls (streamers) move vertically and horizontally that will set you back to restart if you interact with them. Walls of the maze also restrict your movements to apply extra difficulty.

This game has been edited to make use of LDRs as game controllers, using PyFirmata and an Arduino (Note* set the IDE to Standard Firmata(found in IDE examples) to run the Firmata protocol used for PyFirmata). This was done as an optional project for those who wish to try out PyFirmata or as a project example using an Arduino as an alternate game controller device. Circuit diagrams have been included, however the analog pins have been adjusted one up in the script.

When running the script you will find that three folders will be created in the directory the script is in.

Background: will allow you to insert multiple image type files that can be set as a backrgound for the game.

Music: Allows you to insert .mp3 files that will then create a random playlist that will start as you play.

Game_Stats: will contain two .txt files. One will keep track of your highest run/score, while the other will measure the latency of your computer to try and give a unique rendering speed so as to make the gameplay standard throughout any device used. (This was tested on both Ubuntu 16.04 and Windows 7, however it is still a little buggy and your are more than welcome to edit the code to adjust the rendering parameters or the .txt file itself)

Inside game options include:

Play: press enter to start; press spacebar to pause and unpause game.

Settings: press enter Audio: press -r to remove audio, -i to insert playlist, or +- to adjust volume. Background: press -r to remove backround (Black Screen/Classic arcade feel), or -i to insert. Difficulty: press -e for easy, -m for moderate, -h for hard. Reset Hi-score: press -r to reset run/score to 0. Return to Main Menu: press enter to return.

Exit - press enter to leave.

All inside game changes by the user should be updated immediately with your difficulty choice and highest run/score indicated in the top right hand corner. Also during play the right hand corner will indicate the number of runs completed since the start of play.

All in all I hope that you enjoy the gameplay and interact by adding your own favorite game music and backgrounds (however black and white images are preferable. In my experience color images seem to become too distracting)

If you notice any bugs or possible changes that could/should be added or fixed please feel free to notify me Severian-desu-ga.

Much appriciated for your patronage, and have free fun with Roll Along!
