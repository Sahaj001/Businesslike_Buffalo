import sys
import bot
from prompt_toolkit.application import Application
from prompt_toolkit.application.current import get_app
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import HSplit, Layout, VSplit
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import Box, Button, Frame, Label, TextArea
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous

sys.path.append("/Users/sahajsingh/Downloads/Businesslike_Buffalo-main/")


class GameScreen:

    def __init__(self) -> None:
        # game 1
        self.path = "/Users/sahajsingh/Downloads/Businesslike_Buffalo-main/Grid_file/assets/ascii/text/"

        self.bot_player = bot.Bot(2, 2)
        self.top_screen = bot.GameScreen(10, 88, [])

        self.top_screen.render_table(self.bot_player)

        self.button1 = Button(text="1. Play Maze   : ", width=30)
        self.button2 = Button(text="2. Play Riddle : ", width=30)
        self.button3 = Button(text="3. Play Puzzle : ", width=30)
        self.exit_button = Button("Exit", handler=self.do_exit)
        self.width = 35
        self.height = 10
        self.top_text = self.to_str()
        # Styling.
        self.style = Style(
            [
                ("left-pane", "bg:#888800 #000000"),
                ("right-pane", "bg:#00aa00 #000000"),
                ("button", "#ff4000"),
                ("button-arrow", "#440022"),
                ("button focused", "bg:#ff0000"),
                ("text-area focused", "bg:#ff0000"),
            ]
        )

    def bot_key_bindings(self):
        # Key bindings
        self.kb = KeyBindings()

        @self.kb.add("q")
        def _(event):
            "Exit the window."
            event.app.exit()

        self.kb.add("tab")(focus_next)
        self.kb.add("s-tab")(focus_previous)

        @self.kb.add("left")
        def go_left(self):
            self.bot_player.new_pos(self.bot_player.x+2, self.bot_player.y)

    def to_str(self):

        mat = ""

        for i in self.top_screen.table:
            for j in i:
                mat += j

            mat += '\n'

        return mat

    def do_exit():
        get_app().exit()

    def read_text(self, filename: str):
        with open(self.path+filename, 'r') as file:
            data = file.read()
        return data

    def top(self):
        return Frame(
            TextArea(
                text=self.top_text,
                height=18,
                style="#ff0000 bg:#f0f0f0 bold",
            ),
            height=20,
        )

    def middle(self):
        width = self.width
        height = self.height
        return Frame(
            Box(
                HSplit(
                    [
                        VSplit(
                            [
                                Box(
                                    Frame(
                                        TextArea(
                                            text=self.read_text('maze.txt'),
                                            width=width,
                                            height=height,
                                        )
                                    ),
                                    style="bg:#00729c",
                                ),
                                Box(
                                    Frame(
                                        TextArea(
                                            text=self.read_text('riddle.txt'),
                                            width=width,
                                            height=height,
                                        )
                                    ),
                                    style="bg:#00729c",
                                ),
                                Box(
                                    Frame(
                                        TextArea(
                                            text=self.read_text('puzzle.txt'),
                                            width=width,
                                            height=height,
                                        )
                                    ),
                                    style="bg:#00729c",
                                ),
                            ],
                            padding_char='|',
                            padding=1,
                        )
                    ],
                    style="bg:#00729c",
                ),
            )
        )

    def bottom(self):
        return Frame(
            Box(
                HSplit(
                    [
                        Label(text="Press `Tab` to move the focus."),
                        Box(
                            body=HSplit([self.button1, self.button2, self.button3, self.exit_button],
                                        padding=1, padding_char='.'),
                            style="bg:#0f0947",
                            width=35,
                        ),
                    ]
                ),
                style="bg:#00729c"
            ),
        )

    def start_screen(self):

        return Frame(
            Box(
                HSplit([
                    Label(text="Select the game to play : ", style="#b30295"),
                    self.top(),
                    self.middle(),
                    self.bottom()
                ],
                    padding_char='~',
                    padding=1
                ),
                style="bg:#00bbff"
            ),
        )

    def layout(self):
        """
        The layout function calls the container object
        """
        return Layout(self.start_screen(), focused_element=self.exit_button)

    def run(self):
        """
        Calls the run function from Application to lauch the window
        """
        app = Application(layout=self.layout(), full_screen=True, key_bindings=self.kb)
        return app.run()


if __name__ == "__main__":
    # start screen

    game = GameScreen()
    game.run()
    # print("dgfh")
    # for i in range(0,10):
    # bot1.new_pos(bot1.x+1,bot1.y)
