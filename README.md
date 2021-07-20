# Boxed In
Welcome to Boxed In! A terminal based adventure game created in [prompt-toolkit for Python](https://python-prompt-toolkit.readthedocs.io/).

# Gameplay
In Boxed In, you play the character of Bob, a teenager who finds himself to be abducted and left in the outdoors. He quickly finds out though, that his surroundings are anything but normal, and that in reality he's been trapped in a large box.

In order to escape, you'll have to think _inside_ the box because, well, you're Boxed In! You don't have a choice!

## Installation and setup
1. Clone the repository to your local machine.
2. Install the requirements listed in `requirements.txt` (it is recommended that you initialise a virtual environment for this).
3. `cd` into the `src` folder.
4. Run the game by running `python first-screen.py`

while running if it gives an error like module `gi` is not found just do this `pip3 install playsound`

![](https://cdn.discordapp.com/attachments/862342534616842246/866923028292829204/image1.png)



### FRAMEWORK
Prompt-Toolkit

### SYSTEM SUPPORT

It has been tested on Windows, Mac and Linux, so there will be no issues.


### SRC

The src file contains:
bot.py           grid.py         layout.py  person.py      quests.py
entities.py      hangman.py      map.py     play_sound.py  screen.py
first_screen.py  highlighter.py  maze.py    \__pycache__/   test.py


1) bot.py: It contains the script for a moving object on the start screen at the top.
2) grid.py: It is our own rendering engine.
3) layout.py: It contains the script for key binding and game screen.
4) person.py: It contains the player class.
5) quests.py: It contains the script for the quests and implementation.
5) entities.py: It convert the ascii arts into entity object present in the file.
6) hangman.py: It contains the script for a mini-game called hangman.
7) map.py: It contains the entities which are going to rendered on the screen.
8) play_sound.py: Could not be implemented due to time trouble.
9) first_screen.py: It contains the script for our start screen.
10) highlighter.py: It contains the regex lexer used to highlight our entities.
11) maze.py: It contains the script for a mini-game called maze
12) test.py: Used as a testing file to test rendering

NOTE: all the mini-games are included in the main game

### GAME

It is an open-world game with a small map, the user can either choose to do the quests or roam around freely. It is named as Boxed In, everything used in the game are our own creations except the sounds. The player is trapped inside a box. It has to complete some quests to get outside of the box and it depends upon your choices whether he can escape or not. The quests are of numerous types for eg, riddles, maze, hangman and we made our own riddles. Unfortunately there are no easter eggs. 
![](https://cdn.discordapp.com/attachments/863105912599478302/863142004329283604/unknown.png)

While doing some quests you need to get to the right (x,y) coordinate and press 'x', it will open a window you can press 'q' to go back, the controls are:
A/left-arrow-key: It moves the player left.
D/right-arrow-key: It moves the player right.
S/down-arrow-key: It moves the player down.
W/up-arrow-key: It moves the player up.
N: Changes the current message displaying on the screen.
J: Key to react with the riddle (first option).
K: Key to react with the riddle (second option).
L: Key to react with riddle (third option).

![](https://cdn.discordapp.com/attachments/862342534616842246/866923027891093525/image0.png)



![](https://cdn.discordapp.com/attachments/862342534616842246/866923028663107594/image2.png)




![](https://cdn.discordapp.com/attachments/862342534616842246/866923029216100352/image4.png)


### BUGS

1) If the user presses 'exit' then presses 'no' and then presses 'help' and goes back, and then again presses 'exit' it shows the help screen on the start screen.

2) When in a quest if you keep pressing 'n' it skips the quest.

If you encounter some other bugs please make them a issue in our repo.

### CONTRIBUTIONS

1) Axthe_E_I#6328/Sahaj001 - Leader: In the making of start screen, hangman and also implementing sound.
2) rmrf#1236/JRavi2: Layout of the game, map and implementing quests.
3) Cyn1ch0#7454/Cyn1ch0: Making of all the artwork and maze.
4) Vecko#3702/VeckoTheGecko - Idea for the project: Made the entities class, the ascii arts and editing the rendering engine.
5) ГенералМуд#0001/Ibrahim2750mi: Made the rendering engine, the player class, the quests script, the regex highlighter for entities and collision detection.


![](https://cdn.discordapp.com/attachments/862342534616842246/866923028993540107/image3.png)


## DEVLOPER'S NOTE

You will find some files which are not used in the main-game, that is because we were thinking of implementing them but we ran out of time, hope you enjoy playing this
