import re
import time
from prompt_toolkit import styles
from prompt_toolkit.shortcuts.dialogs import message_dialog
from prompt_toolkit.formatted_text import HTML
# import play_sound
import simpleaudio as sa
from prompt_toolkit import styles
from prompt_toolkit.application import Application
from prompt_toolkit.application.current import get_app
from prompt_toolkit.document import Document
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.focus import (
    focus_next, focus_previous
)
from prompt_toolkit.key_binding.key_processor import KeyPressEvent
from prompt_toolkit.layout import HSplit, Layout, VSplit, Window, WindowAlign
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.shortcuts import yes_no_dialog
from prompt_toolkit.styles import Style, style
from prompt_toolkit.widgets import Box, Button, Frame, Label, TextArea

import bot
import layout


# noinspection PyTypeChecker
class GameScreen:
    """Game Screen with a layout of the launch page."""

    def __init__(self) -> None:
        """Initialize the class with attributes like bot and screen."""

        # game 1
        self.path = "../assets/ascii/text/"
        self.launch = True
        self.bot_player = bot.Bot(10, 3)
        self.top_screen = bot.StartScreen(20, 56)

        self.top_screen.render_table(self.bot_player)

        self.button1 = Button(text= " Play ", width=10 ,
                              right_symbol= " ", left_symbol= " ", handler=self.do_exit1)
        self.button2 = Button(text=" Help ", width=30 , 
                              right_symbol= " ", left_symbol= " ", handler=self.do_exit3)
        self.button3 = Button(text=" Exit ", width=30 , 
                              right_symbol= " ", left_symbol= " ", handler=self.do_exit2)
        self.exit_button = Button("Exit", handler=self.do_exit)
        self.width = 35
        self.height = 10
        self.top_text = self.to_str()
        self.xb = 1
        self.yb = 1
        # self.audio = play_sound.PlayAudio('intro_music.wav')
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
        self.gameplay = False
        self.help = False
        self.true_exit = False
        self.container1 = TextArea(text=self.top_text, height=18, style="#ff0000 bg:#f0f0f0 bold")

        # Key bindings
        self.kb = KeyBindings()

        @self.kb.add("q")
        def _exit(event):
            """Exits the windows."""
            get_app().exit()

        self.kb.add("tab")(focus_next)
        self.kb.add("s-tab")(focus_previous)

        @self.kb.add("left")
        def _(event: KeyPressEvent):
            self.bot_player.new_pos(self.bot_player.x, self.bot_player.y - 1)
            new_text = self.top_screen.render_table(self.bot_player)
            self.container1.buffer.document = Document(
                text=new_text, cursor_position=len(new_text)
            )

        @self.kb.add("right")
        def _(event: KeyPressEvent):
            self.bot_player.new_pos(self.bot_player.x, self.bot_player.y + 1)
            new_text = self.top_screen.render_table(self.bot_player)

            self.container1.buffer.document = Document(
                text=new_text, cursor_position=len(new_text)
            )

        @self.kb.add("up")
        def _(event: KeyPressEvent):
            self.bot_player.new_pos(self.bot_player.x - 1, self.bot_player.y)
            new_text = self.top_screen.render_table(self.bot_player)

            self.container1.buffer.document = Document(
                text=new_text, cursor_position=len(new_text)
            )

        @self.kb.add("down")
        def _(event: KeyPressEvent):
            self.bot_player.new_pos(self.bot_player.x + 1, self.bot_player.y)
            new_text = self.top_screen.render_table(self.bot_player)

            self.container1.buffer.document = Document(
                text=new_text, cursor_position=len(new_text)
            )

    def on_invalidate(self, event):
        """ using Invalidate to run the animatation """
        if self.launch is True:
            time.sleep(4)
            self.do_exit()

        if (self.bot_player.y + self.yb) % 50 == 49 and self.yb == 1:
            self.yb = -1

        if (self.bot_player.y + self.yb) == 3 and self.yb == -1:
            self.yb = 1

        if (self.bot_player.x + self.xb) % 15 == 14 and self.xb == 1:
            self.xb = -1

        if (self.bot_player.x + self.xb) == 3 and self.xb == -1:
            self.xb = 1

        self.bot_player.new_pos(self.bot_player.x + self.xb, self.bot_player.y + self.yb)
        new_text = self.top_screen.render_table(self.bot_player)

        self.container1.buffer.document = Document(
            text=new_text
        )

    def to_str(self):
        """ Function to return the table object as string"""

        mat = ""
        for i in self.top_screen.table:
            for j in i:
                mat += j

            mat += '\n'

        return mat

    def do_exit1(self):
        self.gameplay = True
        get_app().exit()
   
    def do_exit2(self):
        self.true_exit = True
        get_app().exit()

    def do_exit(self):
        get_app().exit()
        
    def do_exit3(self):
        self.help = True
        get_app().exit()

    def read_text(self, filename: str):
        """ reading the text file """
        with open(self.path + filename, 'r', encoding="utf-8") as file:
            data = file.read()
        return data

    def top(self):
        """Top frame of the game screen"""
        return Frame(
            self.container1,
            height=20,
        )

    def middle(self):
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
                                            text=self.read_text('boxedIn.txt'),
                                            style="#f03934 bg:#320420",
                                            width=88,
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
                            body=HSplit([self.button1, self.button2, self.button3],
                                        padding=1, padding_char='-'),
                            style="bg:#0f0947 #f03934",
                            width=35,
                            height=7,
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
                    self.top(),
                    self.middle(),
                    self.bottom()
                ],
                    padding=1,
                    align=WindowAlign.CENTER
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

        with open(f"{self.path}bot2.txt", 'r', encoding="utf-8") as file:
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

        audio_file_intro = sa.WaveObject.from_wave_file('../assets/audio/intro_music.wav')
        audio_file_intro.play()
        app1.run()
        self.launch = False

        app = Application(layout=self.layout(), full_screen=True, key_bindings=self.kb,
                          mouse_support=True, refresh_interval=0.2, on_invalidate=self.on_invalidate)
        
        app.run()
        while(True):
            if self.true_exit == True:
                result = yes_no_dialog(
                    title='Exit the game',
                    text = 'Do you want to confirm ?'
                ).run()
                if result == True:
                    return
                else:
                    self.true_exit == False
                    app.run()
                    
            elif self.help == True:
                message_dialog(
                    title='Help',
                    text=HTML('<style fg="ansired">Press - X interact with objects\nArrow keys or WASD to move the player\nAnd remember, don\'t you dare think outside the box (if you wanna live that is).\nJust politely follow the instructions, and you just might escape!</style>')
                ).run()
                self.help == False
                app.run()
            
            self.true_exit == False
            self.help == False
            
            if self.gameplay == True:
                layoutScreen = layout.Game()
                layoutScreen.run()
                return
        


if __name__ == "__main__":
    # start screen

    game = GameScreen()
    game.run()
