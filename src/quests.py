import json


class Quest:
    def __init__(self):
        self.quest_1 = True
        self.quest_2 = False
        self.quest_3 = False
        self.quest_4 = False
        self.open_world = False
        self.witch = True
        self.mcq = False
        self.progression = (0, 0)

        self.text_variables = {1: self.quest_1_messages, 2: self.quest_2_messages,
                          3: self.quest_3_messages, 4: self.quest_4_messages}

        for script_value in range(1, 5):
            with open(f"./script/quest_{script_value}_messages.txt") as f:
                self.text_variables[script_value] = json.load(f)

    def reset(self):
        self.progression = (0, 0)
