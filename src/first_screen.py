import bot
import play_sound
import playsound
from prompt_toolkit.application import Application
from prompt_toolkit.application.current import get_app
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.document import Document
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.key_processor import KeyPressEvent
from prompt_toolkit.layout import HSplit, Layout, VSplit, Window, WindowAlign
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import Box, Button, Frame, Label, TextArea
import time


class GameScreen:

    """
    Game Screen with a layout of the launch page
    """
    def __init__(self) -> None:
        """
        Initialize the class with attributes like bot and screen
        """
        # game 1
        self.path = "/assets/ascii/text/"
        self.launch = True
        self.bot_player = bot.Bot(10, 3)
        self.top_screen = bot.GameScreen(20, 60, [])

        self.top_screen.render_table(self.bot_player)

        self.button1 = Button(text="1. Play Maze   : ", width=30)
        self.button2 = Button(text="2. Play Riddle : ", width=30)
        self.button3 = Button(text="3. Play Puzzle : ", width=30)
        self.exit_button = Button("Exit", handler=self.do_exit)
        self.width = 35
        self.height = 10
        self.top_text = self.to_str()
        self.xb = 1
        self.yb = 1
        self.audio = play_sound.PlayAudio('intro_music.wav')
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
        self.container1 = TextArea(text=self.top_text, height=18, style="#ff0000 bg:#f0f0f0 bold")

        # Key bindings
        self.kb = KeyBindings()

        @self.kb.add("q")
        def _exit(event):
            "Exit the window."
            self.do_exit()

        self.kb.add("tab")(focus_next)
        self.kb.add("s-tab")(focus_previous)

        @self.kb.add("left")
        def _(event: KeyPressEvent):
            self.bot_player.new_pos(self.bot_player.x, self.bot_player.y-1)
            new_text = self.top_screen.render_table(self.bot_player)
            self.container1.buffer.document = Document(
                text=new_text, cursor_position=len(new_text)
            )

        @self.kb.add("right")
        def _(event: KeyPressEvent):
            self.bot_player.new_pos(self.bot_player.x, self.bot_player.y+1)
            new_text = self.top_screen.render_table(self.bot_player)

            self.container1.buffer.document = Document(
                text=new_text, cursor_position=len(new_text)
            )

        @self.kb.add("up")
        def _(event: KeyPressEvent):
            self.bot_player.new_pos(self.bot_player.x-1, self.bot_player.y)
            new_text = self.top_screen.render_table(self.bot_player)

            self.container1.buffer.document = Document(
                text=new_text, cursor_position=len(new_text)
            )

        @self.kb.add("down")
        def _(event: KeyPressEvent):
            self.bot_player.new_pos(self.bot_player.x+1, self.bot_player.y)
            new_text = self.top_screen.render_table(self.bot_player)

            self.container1.buffer.document = Document(
                text=new_text, cursor_position=len(new_text)
            )

    def on_invalidate(self, event):
        """ using Invalidate to run the animatation """
        if self.launch is True:
            time.sleep(4)
            self.do_exit()

        if (self.bot_player.y+self.yb) % 50 == 49 and self.yb == 1:
            self.yb = -1

        if (self.bot_player.y+self.yb) == 3 and self.yb == -1:
            self.yb = 1

        if (self.bot_player.x+self.xb) % 15 == 14 and self.xb == 1:
            self.xb = -1

        if (self.bot_player.x+self.xb) == 3 and self.xb == -1:
            self.xb = 1

        self.bot_player.new_pos(self.bot_player.x+self.xb, self.bot_player.y+self.yb)
        new_text = self.top_screen.render_table(self.bot_player)

        self.container1.buffer.document = Document(
            text=new_text, cursor_position=len(new_text)
        )

    def to_str(self):
        """ Function to return the table object as string"""

        mat = ""
        for i in self.top_screen.table:
            for j in i:
                mat += j

            mat += '\n'

        return mat

    def do_exit(self):
        get_app().exit()

    def read_text(self, filename: str):
        """ reading the text file """
        with open(self.path+filename, 'r') as file:
            data = file.read()
        return data

    def top(self):
        """Top frame of the game screen"""
        return Frame(
            self.container1,
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
        return Layout(self.start_screen(), focused_element=self.container1)

    def run(self):
        """
        Calls the run function from Application to lauch the window
        """

        with open("bot2.txt", 'r') as file:
            bt2 = file.read()
        body = Window(
            FormattedTextControl(bt2),
            width=100,
            ignore_content_width=True,
            style="bg:#454545 #d200ff",
            align=WindowAlign.LEFT,
            height=300
        )

        app1 = Application(layout=Layout(body),
                           full_screen=True, key_bindings=self.kb, refresh_interval=1,
                           on_invalidate=self.on_invalidate)

        playsound.playsound('intro_music.mp3', False)
        app1.run()
        self.launch = False

        app = Application(layout=self.layout(), full_screen=True, key_bindings=self.kb,
                          mouse_support=True, refresh_interval=0.2, on_invalidate=self.on_invalidate)

        app.run()


if __name__ == "__main__":
    # start screen

    game = GameScreen()
    game.run()
    # print("dgfh")
    # for i in range(0,10):
    # bot1.new_pos(bot1.x+1,bot1.y)
