import json


class Quest:
    """Class to manage all the quests"""

    def __init__(self):
        self.quest_1 = True
        self.quest_2 = False
        self.quest_3 = False
        self.quest_4 = False
        self.open_world = False
        self.witch = True
        self.mcq = False
        self.progression = [-1, -1]

        self.dialogues = {1: {}, 2: {},
                          3: {}, 4: {}}

        for script_value in range(1, 5):
            with open(f"./quest_{script_value}_texts.json") as f:
                self.dialogues[script_value] = json.load(f)

    def reset(self) -> None:
        """Reset the quest progression"""
        self.progression = [-1, -1]

    def is_complete(self, quest: int) -> bool:
        """Check whether the given quest is complete or not"""
        if quest == 1:
            if self.progression[0] == 3:
                return True
        return False

    def get_message(self, quest: int, option: int = -1) -> str:
        """Return the game response for the given quest"""
        if quest == 1:
            if option == -1:
                if self.progression[0] in (0, 1):
                    self.progression[0] = 1
                    return self.dialogues[quest]["narrator"][self.progression[0]]
            elif self.progression[1] == -1:
                if self.progression[0] == -1:
                    self.progression[0] = 0
                    return self.dialogues[quest]["narrator"][self.progression[0]]
                self.progression[1] = 0
                return self.dialogues[quest]["witch"][self.progression[1]]
            elif self.progression[1] == 4:
                self.progression[0] = 2
                self.progression[1] = 7
                return self.dialogues[quest]["narrator"][self.progression[0]]
            elif option == 1:
                if self.progression[1] == 0:
                    self.reset()
                    return self.dialogues[quest]["witch"][1]
                elif self.progression[1] == 3:
                    self.reset()
                    return self.dialogues[quest]["witch"][5]
                elif self.progression[0] == 2:
                    self.progression[0] = 3
                    return self.dialogues[quest]["narrator"][self.progression[0]]
            elif option == 2:
                if self.progression[1] == 0:
                    self.progression[1] = 3
                    return self.dialogues[quest]["witch"][self.progression[1]]
                elif self.progression[1] == 3:
                    self.progression[1] = 4
                    return self.dialogues[quest]["witch"][self.progression[1]]
                elif self.progression[0] == 2:
                    self.progression[0] = 4
                    return self.dialogues[quest]["narrator"][self.progression[0]]
            elif option == 3:
                if self.progression[1] == 0:
                    self.reset()
                    return self.dialogues[quest]["witch"][2]
                elif self.progression[1] == 3:
                    self.reset()
                    return self.dialogues[quest]["witch"][5]
                elif self.progression[0] == 2:
                    return self.dialogues[quest]["narrator"][self.progression[0]]
        return ""
