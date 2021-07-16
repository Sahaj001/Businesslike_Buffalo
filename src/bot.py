"""
This is a bot class which moves around the grid
"""
import numpy as np

path = "assets/ascii/text"


class Bot:

    def __init__(self, x: int, y: int, facing: str = str("right"), botfile: str = str("bot.txt")) -> None:
        """
        Bot is an entity in a game, can be made controlable
        :param x : x position of bot in Grid
        :param y : y position of bot in Grid
        :facing : the direction in which bot is facing [left, right]
        """

        self.x = x
        self.y = y
        self.facing = facing
        self.path = "/assets/ascii/text/"
        self.ascii_bot, self.height, self.width = self.read_text(botfile)

    def read_text(self, filename: str):
        with open(self.path+filename, 'r') as file:
            data = file.readlines()
        width = max([len(line) for line in data])
        height = len(data)
        data = [line[0:-1] + (width - len(line)) * " " for line in data]
        data = np.array([list(line) for line in data])
        return data, height, width

    def new_pos(self, new_x: int, new_y: int):
        """
        Insert new position of the bot
        :param x: new x position
        :param y: new y position
        """
        self.x = new_x
        self.y = new_y


class GameScreen:

    def __init__(self, height: int, width: int, table):
        """
        Screen at the start of the game
        :param height : height of the Screen
        :param width : width of the Screen
        :param table : render table
        """

        self.height = height
        self.width = width
        self.table = np.full((self.height, self.width), " ")

    def render_table(self, bot: Bot):
        """"
        render the table screen for bot
        :param bot : Bot class
        """
        self.delete_bot(bot)
        self.table[bot.x:bot.x+bot.height, bot.y:bot.y+bot.width-1] = bot.ascii_bot
        return self.print_st(self.table)

    def delete_bot(self, bot: Bot):
        """
        deleting the previous position of the bot
        """
        self.table[bot.x-1:bot.x+bot.height+1, bot.y-1:bot.y+bot.width+1] = " "

    def print_st(self, table):
        st = ""
        for i in table:
            for j in i:
                st += j
            st += '\n'
        return st

# if __name__ == "__main__":
    # bot1 = Bot(1, 2)

    # screen1 = GameScreen(10, 40, [])
    # screen1.render_table(bot1)
    # print_st(screen1.table)

    # bot1.new_pos(bot1.x+4, bot1.y+4)
    # screen1.render_table(bot1)

    # print_st(screen1.table)
