"""This is a bot class which moves around the grid."""
import numpy as np

path = "../assets/ascii/text"


class Bot:
    """It is a moving object on the start screen in the white box."""

    def __init__(self, x: int, y: int, facing: str = str("right"), botfile: str = str("bot.txt")) -> None:
        """Bot is an entity in a game, can be made controlable.

        :param x : x position of bot in Grid
        :param y : y position of bot in Grid
        :facing : the direction in which bot is facing [left, right]
        """
        self.x = x
        self.y = y
        self.facing = facing
        self.path = "../assets/ascii/text/"
        self.ascii_bot, self.height, self.width = self.read_text(botfile)

    def read_text(self, filename: str):
        """Reads bot.txt.

        :param filename: The filename it needs to read.
        :return:
        """
        with open(self.path + filename, 'r', encoding="utf-8") as file:
            data = file.readlines()
        width = max([len(line) for line in data])
        height = len(data)
        data = [line[0:-1] + (width - len(line)) * " " for line in data]
        data = np.array([list(line) for line in data])
        return data, height, width

    def new_pos(self, new_x: int, new_y: int) -> None:
        """Insert new position of the bot.

        :param new_x: new x position
        :param new_y: new y position
        """
        self.x = new_x
        self.y = new_y


class StartScreen:
    """The start screen which displays the bot."""

    def __init__(self, height: int, width: int) -> None:
        """Screen at the start of the game.

        :param height : height of the Screen
        :param width : width of the Screen
        :param table : render table
        """
        self.height = height
        self.width = width
        self.table = np.full((self.height, self.width), " ")

    def print_st(self) -> str:
        """Converts the matrix into a string. It is equivalent as ''.join(np.c_(self.table, "\n").ravel().tolist())."""
        st = ""
        for i in self.table:
            for j in i:
                st += j
            st += '\n'
        return st

    def render_table(self, bot: Bot) -> str:
        """Render the table screen for bot.

        :param bot : Bot class
        """
        self.delete_bot(bot)
        self.table[bot.x:bot.x + bot.height, bot.y:bot.y + bot.width - 1] = bot.ascii_bot
        return self.print_st()

    def delete_bot(self, bot: Bot) -> None:
        """Deleting the previous position of the bot.

        :param bot: Bot class
        """
        self.table[bot.x - 1:bot.x + bot.height + 1, bot.y - 1:bot.y + bot.width + 1] = " "
