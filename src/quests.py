import json

from hangman import Hangman
from maze import Maze


class Quest:
    """Class to manage all the quests"""

    def __init__(self):
        self.open_world = False
        self.witch = True
        self.mcq = False
        self.progression = [-1, -1, -1, -1]
        self.current_msg = ""

        self.maze = Maze(13, 5, 5, scale=3)
        self.hangman = Hangman("helloWorld", 9)

        self.dialogues = {1: {}, 2: {},
                          3: {}, 4: {}}

        for script_value in range(1, 5):
            with open(f"../assets/quests/quest_{script_value}_texts.json") as f:
                self.dialogues[script_value] = json.load(f)

    def reset(self) -> None:
        """Reset the quest progression"""
        self.progression = [-1, -1, -1, -1]

    def is_complete(self, quest: int) -> bool:
        """Check whether the given quest is complete or not"""
        if quest == 1:
            if self.progression[0] == 3:
                self.reset()
                return True
        if quest == 2:
            if self.progression[3] == 3:
                self.reset()
                return True
        if quest == 3:
            if self.progression[1] == 1:
                self.reset()
                return True
            elif self.progression[0] == 4:
                self.reset()
                return True
        if quest == 4:
            if self.progression[1] == 0:
                return True
        return False

    def get_message(self, quest: int, option: int = -1, alphabet: chr = '*') -> str:
        """Return the game response for the given quest"""
        # The different scenarios for Quest 1
        if quest == 1:
            if option == -1:
                if self.progression[0] in (0, 1):
                    self.progression[0] = 1
                    self.current_msg = self.dialogues[quest]["narrator"][self.progression[0]]
                    return self.current_msg
                else:
                    return self.current_msg
            elif option == -2:
                if self.progression[1] == 4:
                    self.progression[0] = 2
                    self.progression[1] = 7
                    self.current_msg = self.dialogues[quest]["narrator"][self.progression[0]]
                    return self.current_msg
                elif self.progression[0] not in (2, 3):
                    self.progression[0] = 1
                    self.progression[1] = 0
                    self.current_msg = self.dialogues[quest]["narrator"][self.progression[0]]
                    return self.current_msg
                else:
                    return self.current_msg
            elif self.progression[1] == -1:
                if self.progression[0] == -1:
                    self.progression[0] = 0
                    self.current_msg = self.dialogues[quest]["narrator"][self.progression[0]]
                    return self.current_msg
                elif option not in (1, 2, 3):
                    self.progression[1] = 0
                    self.current_msg = self.dialogues[quest]["witch"][self.progression[1]]
                    return self.current_msg
                else:
                    return self.dialogues[quest]["narrator"][self.progression[0]]
            elif option == 0:
                if self.progression[0] == 2:
                    return self.dialogues[quest]["narrator"][self.progression[0]]
                else:
                    return self.dialogues[quest]["witch"][self.progression[1]]
            elif option == 1:
                if self.progression[1] in (1, 2, 4, 5):
                    self.current_msg = self.dialogues[quest]["witch"][6]
                    return self.current_msg
                if self.progression[1] == 0:
                    self.reset()
                    self.current_msg = self.dialogues[quest]["witch"][1]
                    return self.current_msg
                elif self.progression[1] == 3:
                    self.reset()
                    self.current_msg = self.dialogues[quest]["witch"][5]
                    return self.current_msg
                elif self.progression[0] == 2:
                    self.progression[0] = 3
                    self.current_msg = self.dialogues[quest]["narrator"][self.progression[0]]
                    return self.current_msg
                else:
                    self.current_msg = self.dialogues[quest]["narrator"][self.progression[0]]
                    return self.current_msg
            elif option == 2:
                if self.progression[1] in (1, 2, 4, 5):
                    self.current_msg = self.dialogues[quest]["witch"][self.progression[1]]
                    return self.current_msg
                if self.progression[1] == 0:
                    self.progression[1] = 3
                    self.current_msg = self.dialogues[quest]["witch"][self.progression[1]]
                    return self.current_msg
                elif self.progression[1] == 3:
                    self.progression[1] = 4
                    self.current_msg = self.dialogues[quest]["witch"][self.progression[1]]
                    return self.current_msg
                elif self.progression[0] == 2:
                    self.progression[0] = 4
                    self.current_msg = self.dialogues[quest]["narrator"][self.progression[0]]
                    return self.current_msg
                else:
                    return self.current_msg
            elif option == 3:
                if self.progression[1] in (1, 2, 4, 5):
                    self.current_msg = self.dialogues[quest]["witch"][self.progression[1]]
                    return self.current_msg
                if self.progression[1] == 0:
                    self.reset()
                    self.current_msg = self.dialogues[quest]["witch"][2]
                    return self.current_msg
                elif self.progression[1] == 3:
                    self.reset()
                    self.current_msg = self.dialogues[quest]["witch"][5]
                    return self.current_msg
                elif self.progression[0] == 2:
                    self.current_msg = self.dialogues[quest]["narrator"][self.progression[0]]
                    return self.current_msg
                else:
                    return self.current_msg
            else:
                return self.current_msg

        # The different scenarios for Quest 2
        elif quest == 2:
            if option == -1:
                if self.progression[0] == -1:
                    self.progression[0] = 0
                    self.current_msg = self.dialogues[quest]["narrator"][self.progression[0]]
                    return self.current_msg
                elif self.progression[0] == 0:
                    self.progression[0] = 1
                    self.current_msg = self.dialogues[quest]["narrator"][self.progression[0]]
                    return self.current_msg
                else:
                    return self.current_msg
            elif option == -2:
                if self.progression[3] in (2, 3):
                    self.current_msg = self.dialogues[quest]["System"][self.progression[3]]
                    return self.current_msg
                else:
                    self.reset()
                    self.progression[0] = 1
                    self.current_msg = self.dialogues[quest]["narrator"][self.progression[0]]
                    return self.current_msg
            elif option == 0:
                if not alphabet == '*':
                    if self.hangman.chance > 0:
                        self.hangman.input_letter(alphabet)
                        self.current_msg = self.hangman.hangman_str() + "\n" + self.hangman.print_word
                        if self.hangman.game_result():
                            self.current_msg += "\nYou saved Test1!\n\nYou see an envolope. Press 'J' to open it"
                            self.progression[3] = 6
                        return self.current_msg
                    else:
                        self.progression[3] = 7
                        return "You failed Test1, may his soul rest in piece.\nYou see an envolope\nPress 'J' to open"
                elif self.progression[1] == -1:
                    self.progression[1] = 0
                    return self.dialogues[quest]["Test1"][self.progression[1]]
                elif self.progression[3] == 2:
                    self.progression[3] = 4
                    return self.dialogues[quest]["System"][self.progression[3]]
                elif self.progression[3] == 3:
                    return self.dialogues[quest]["System"][self.progression[3]]
                elif self.progression[3] == 4:
                    return self.dialogues[quest]["System"][self.progression[3]]
            elif option == 1:
                if self.progression[2] == -1:
                    self.progression[2] = 0
                    return self.dialogues[quest]["Test0"][self.progression[2]]
                elif self.progression[1] == 0:
                    self.progression[1] = 1
                    self.progression[3] = 0
                    return self.dialogues[quest]["Test1"][self.progression[1]] + \
                        self.dialogues[quest]["System"][self.progression[3]]
                elif self.progression[3] == 0:
                    self.progression[3] = 1
                    return self.dialogues[quest]["System"][self.progression[3]]
                elif self.progression[3] == 1:
                    self.progression[3] = 2
                    self.witch = False
                    return self.dialogues[quest]["System"][self.progression[3]]
                elif self.progression[3] == 4:
                    self.progression[3] = 5
                    return self.dialogues[quest]["System"][self.progression[3]]
                elif self.progression[3] == 5:
                    self.current_msg = self.hangman.hangman_str() + "\n" + self.hangman.hangman_str()
                    return self.current_msg
            elif option == 2:
                if self.progression[3] == 1:
                    self.progression[3] = 3
                    self.current_msg = self.dialogues[quest]["System"][self.progression[3]]
                    return self.current_msg
                elif self.progression[1] == 1:
                    return self.dialogues[quest]["Test1"][self.progression[1]]
                elif self.progression[2] == 0:
                    return self.dialogues[quest]["Test0"][self.progression[2]]
                elif self.progression[1] == 0:
                    return self.dialogues[quest]["Test1"][self.progression[1]]
            elif option == 3:
                if self.progression[3] == 1:
                    return self.dialogues[quest]["System"][self.progression[3]]
                if self.progression[1] == 1:
                    return self.dialogues[quest]["Test1"][self.progression[1]] + \
                        self.dialogues[quest]["System"][self.progression[3]]
                elif self.progression[2] == 0:
                    return self.dialogues[quest]["Test0"][self.progression[2]]
                elif self.progression[1] == 0:
                    return self.dialogues[quest]["Test1"][self.progression[1]]

        # The different scenarios for Quest 3
        elif quest == 3:
            if option == 0:
                if self.witch and self.progression[1] == -1:
                    self.progression[1] = 0
                    return self.dialogues[quest]["witch"][self.progression[1]]
                elif self.witch and self.progression[1] == 0:
                    self.progression[1] = 1
                    return self.dialogues[quest]["witch"][self.progression[1]]
                elif self.progression[0] == -1:
                    self.progression[0] = 0
                    return self.dialogues[quest]["system"][self.progression[0]]
                elif self.progression[0] == 4:
                    return self.dialogues[quest]["system"][self.progression[0]]
            elif option == 1:
                if self.progression[0] == -1:
                    self.progression[0] = 0
                    return self.dialogues[quest]["system"][self.progression[0]]
                if self.progression[0] == 0:
                    return self.dialogues[quest]["system"][5] + self.dialogues[quest]["system"][self.progression[0]]
                if self.progression[0] == 1:
                    return self.dialogues[quest]["system"][5] + self.dialogues[quest]["system"][self.progression[0]]
                if self.progression[0] == 2:
                    return self.dialogues[quest]["system"][5] + self.dialogues[quest]["system"][self.progression[0]]
                if self.progression[0] == 3:
                    return self.dialogues[quest]["system"][5] + self.dialogues[quest]["system"][self.progression[0]]
            elif option == 2:
                if self.progression[0] == 0:
                    return self.dialogues[quest]["system"][5] + self.dialogues[quest]["system"][self.progression[0]]
                if self.progression[0] == 1:
                    return self.dialogues[quest]["system"][5] + self.dialogues[quest]["system"][self.progression[0]]
                if self.progression[0] == 2:
                    return self.dialogues[quest]["system"][5] + self.dialogues[quest]["system"][self.progression[0]]
                if self.progression[0] == 3:
                    self.progression[0] = 4
                    return self.dialogues[quest]["system"][self.progression[0]]
            elif option == 3:
                if self.progression[0] == 0:
                    self.progression[0] = 1
                    return self.dialogues[quest]["system"][self.progression[0]]
                if self.progression[0] == 1:
                    self.progression[0] = 2
                    return self.dialogues[quest]["system"][self.progression[0]]
                if self.progression[0] == 2:
                    self.progression[0] = 3
                    return self.dialogues[quest]["system"][self.progression[0]]
                if self.progression[0] == 3:
                    return self.dialogues[quest]["system"][5] + self.dialogues[quest]["system"][self.progression[0]]

        # The different scenarios for Quest 4
        elif quest == 4:
            if option == 0:
                if self.progression[0] == -1:
                    self.progression[0] = 0
                    self.current_msg = self.dialogues[quest]["guy"][self.progression[0]]
                    return self.current_msg
                elif self.progression[0] == 0:
                    self.current_msg = self.dialogues[quest]["guy"][self.progression[0]]
                    return self.current_msg
                else:
                    return self.current_msg
            elif option == -2:
                if self.progression[1] == -1:
                    self.progression[1] = 0
                    self.current_msg = self.dialogues[quest]["narrator"][self.progression[1]]
                    return self.current_msg
                else:
                    return self.current_msg
            elif option in (2, 3):
                if self.progression[0] in (0, 1):
                    self.progression[0] = 2
                    self.current_msg = self.dialogues[quest]["guy"][self.progression[0]]
                    return self.current_msg
            elif option == 1:
                self.progression[0] = 2
                self.current_msg = self.dialogues[quest]["guy"][self.progression[0]]
                return self.current_msg
            elif alphabet == "w":
                self.maze.move("up")
                if self.maze.num_keys == self.maze.keys_collected:
                    self.progression[1] = 0
                    self.current_msg = "You collected all the keys!"
                    return self.current_msg
                self.current_msg = self.maze.display(self.maze.cells)
                return self.current_msg
            elif alphabet == "a":
                self.maze.move("left")
                if self.maze.num_keys == self.maze.keys_collected:
                    self.progression[1] = 0
                    self.current_msg = "You collected all the keys!"
                    return self.current_msg
                self.current_msg = self.maze.display(self.maze.cells)
                return self.current_msg
            elif alphabet == "s":
                self.maze.move("down")
                if self.maze.num_keys == self.maze.keys_collected:
                    self.progression[1] = 0
                    self.current_msg = "You collected all the keys!"
                    return self.current_msg
                self.current_msg = self.maze.display(self.maze.cells)
                return self.current_msg
            elif alphabet == "d":
                self.maze.move("right")
                if self.maze.num_keys == self.maze.keys_collected:
                    self.progression[1] = 0
                    self.current_msg = "You collected all the keys!"
                    return self.current_msg
                self.current_msg = self.maze.display(self.maze.cells)
                return self.current_msg
        if quest == 5:
            return self.dialogues[quest-1]["narrator"][0]
        return ""
