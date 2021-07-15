# from numpy import unicode_
import pygments
import pygments.lexers
from prompt_toolkit.application import Application
from prompt_toolkit.formatted_text import PygmentsTokens
from prompt_toolkit.key_binding import KeyBindings, KeyPressEvent
from prompt_toolkit.layout.containers import (
    Float, FloatContainer, HSplit, Window, WindowAlign
)
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import Frame

from entities import Bar, Fountain, Tree, WitchHut
from person import Person
from screen import Screen


class Game:
    """Specifies the main layout of the game i.e. the play area and the rest of the UI"""

    def __init__(self):
        """Initializes the Layout"""
        self.screen = Screen(88, 24)
        self.tree = Tree(10, 4, 5, unique_name="Tree1")
        self.player = Person(84, 20, 5, unique_name="Bob")
        self.bar = Bar(50, 3, 5, unique_name="bar1")
        self.fountian = Fountain(30, 5, 5, unique_name="fountain1")
        self.witch_hut = WitchHut(60, 10, 4, "witch_hut1")
        self.screen.insert_entity(self.tree)
        self.screen.insert_entity(self.bar)
        self.screen.insert_entity(self.fountian)
        self.screen.insert_entity(self.witch_hut, screen=4)
        self.screen.insert_entity(self.player, True)

        self.maze_trigger_coords = (54, 10)  # (x, y) of the bar door
        self.hangman_trigger_coords = (0, 0)  # (x, y) of a tree
        self.puzzle_trigger_coords = (64, 16)  # (x, y) of the fountain

        self.game_progression = 0  # The overall game progression (used for narrator messages)
        self.active_quest = -1  # Is a quest currently active, if yes -> (1=Puzzle, 2=Maze)
        self.puzzle_progression = 0  # The Progression within the puzzle quest (Used for dialogue tracking)
        self.completed_quests = 0  # The total number of quests completed

        # TODO: Complete the messages
        self.messages = ["Welcome Test0 you have been abducted to be tested in our facility. \nYou may think what "
                         "is this surrounding, well you are basically in a box of imagination, the more you explore "
                         "the more deeper it gets.\nComplete my deeds and you shall be free.\nFor a hint, go look for"
                         " a witch, she has a potion that i looovee to drink, but be aware she doesn't like stangers.",
                         "Look who's back, you sure didn’t fail me, now go ahead and take a sip of the potion\n(J) "
                         "Drink Potion\n(K) Refuse", "Good. I like Obendient Subjects", "Wrong choice!\nGame Over"]
        self.puzzle_messages = ["Witch: Oh my who are you, do not come near me or I will curse you.\n(J) run back, "
                                "(K) ask the potion, (L) charge her", "Narrator: You Coward!", "The witch curses "
                                "you and kicks you out!",
                                "Witch: Oh you must be sent by ‘them’ well to get this potion you need to solve "
                                "\nthis riddle for me.\nThere is a circular platform with a large rod having its "
                                "length same as the\nradius of the platform, with its one kept at the center.\nIt "
                                "moves 90 degree in z axis and burst in thin strips equally and lands at the\nedge "
                                "of the circle. Which shape does it form?\n\n(J) Sphere, (K) Hemisphere, (L) Cone",
                                "There you go my boy here is the potion.", "Wrong answer my boy!",
                                "Press Q to go back"]
        self.current_message = 0
        self.lexer = pygments.lexers.load_lexer_from_file("highlighter.py", lexername="CustomLexer")
        self.style = Style.from_dict({
            "pygments.player": "#0000ff",
            "pygments.leaves": "#00cd00",
            "pygments.trunk": "#964B00",
            "pygments.bar": "bg:#A55D47 #000000",
            "pygments.fountainbase": "#ff7a7a",
            "pygments.water": "#00bafd",
            "pygments.wall.inescapable": "bg:#ed0000"
        })

        tokens = list(pygments.lex(str(self.screen.render()), lexer=self.lexer))

        self.game_field = Frame(
            body=Window(FormattedTextControl(
                text=PygmentsTokens(tokens)
            )),
            style="bg:#000000"
        )

        self.message_box = Frame(
            body=Window(
                FormattedTextControl(self.messages[self.current_message]),
                align=WindowAlign.CENTER
            ),
            title="Narrator (Press 'n' for next Message)",
            height=8
        )

        self.container = HSplit(
            [
                self.game_field,
                Window(height=1, char="-", style="class:line"),
                self.message_box,
            ]
        )

        self.body = FloatContainer(
            content=self.container,
            floats=[
                Float(
                    Frame(
                        Window(FormattedTextControl("Quests completed: 0/3"), width=22, height=1),
                    ),
                    right=5,
                    top=2,
                )
            ]
        )

        self.application = Application(
            layout=Layout(self.body),
            key_bindings=self.get_key_bindings(),
            mouse_support=True,
            full_screen=True,
            style=self.style,
            refresh_interval=0.5,
        )

    def get_key_bindings(self) -> KeyBindings:
        """Add different key bindings to control the player/UI

        :return: KeyBindings Object
        """
        kb = KeyBindings()

        # Exit
        @kb.add("c-c")
        @kb.add("c-q")
        def _(event: KeyPressEvent) -> None:
            event.app.exit()

        # Movement
        @kb.add("a")
        @kb.add("left")
        def go_left(event: KeyPressEvent) -> None:
            if self.active_quest == -1:
                self.player.move('left', self.screen.get_current_screen())
                self.screen.update_entity(self.player, True)

                new_text = self.screen.render()
                tokens = list(pygments.lex(new_text, lexer=self.lexer))

                self.game_field.body = Window(
                    FormattedTextControl(
                        text=PygmentsTokens(tokens)
                    ))

        @kb.add("d")
        @kb.add("right")
        def go_right(event: KeyPressEvent) -> None:
            if self.active_quest == -1:
                self.player.move('right', self.screen.get_current_screen())
                self.screen.update_entity(self.player, True)

                new_text = self.screen.render()
                tokens = list(pygments.lex(new_text, lexer=self.lexer))

                self.game_field.body = Window(
                    FormattedTextControl(
                        text=PygmentsTokens(tokens)
                    ))

        @kb.add("w")
        @kb.add("up")
        def go_up(event: KeyPressEvent) -> None:
            if self.active_quest == -1:
                self.player.move('up', self.screen.get_current_screen())
                self.screen.update_entity(self.player, True)

                new_text = self.screen.render()
                tokens = list(pygments.lex(new_text, lexer=self.lexer))

                self.game_field.body = Window(
                    FormattedTextControl(
                        text=PygmentsTokens(tokens)
                    ))

        @kb.add("s")
        @kb.add("down")
        def go_down(event: KeyPressEvent) -> None:
            if self.active_quest == -1:
                self.player.move('down', self.screen.get_current_screen())
                self.screen.update_entity(self.player, True)

                new_text = self.screen.render()
                tokens = list(pygments.lex(new_text, lexer=self.lexer))

                self.game_field.body = Window(
                    FormattedTextControl(
                        text=PygmentsTokens(tokens)
                    ))

        # Action Key
        @kb.add("x")
        def action(event: KeyPressEvent) -> None:
            if (self.player.x, self.player.y) == self.maze_trigger_coords:
                self.active_quest = 2
                self.body.floats.append(
                    Float(
                        Frame(
                            Window(FormattedTextControl("Render the maze here"), width=88, height=24),
                        )
                    )
                )
                self.message_box.body = Window(
                    FormattedTextControl("Start the maze"),
                    align=WindowAlign.CENTER
                )
            elif (self.player.x, self.player.y) == self.hangman_trigger_coords:
                self.message_box.body = Window(
                    FormattedTextControl("Start the hangman game"),
                    align=WindowAlign.CENTER
                )
            elif (self.player.x, self.player.y) == self.puzzle_trigger_coords:
                self.active_quest = 1
                self.body.floats = [
                    Float(
                        Frame(
                            Window(FormattedTextControl(self.puzzle_messages[0]), width=88, height=24),
                        )
                    )
                ]
                self.message_box.body = Window(
                    FormattedTextControl("Start the puzzles game"),
                    align=WindowAlign.CENTER
                )
            else:
                self.message_box.body = Window(
                    FormattedTextControl(str(self.player.x) + " " + str(self.player.y)),
                    align=WindowAlign.CENTER
                )

        # Keys for in-quest control (Similar for all 'j', 'k', and 'l' keybindings)
        @kb.add("j")
        def quest_option_1(event: KeyPressEvent) -> None:
            if self.active_quest == 1:  # If puzzle quest is active
                if self.puzzle_progression == 0:  # First question
                    text = self.puzzle_messages[0] + \
                        "\n\n" + self.puzzle_messages[1] + \
                        "\n\n" + self.puzzle_messages[6]
                    self.body.floats = [
                        Float(
                            Frame(
                                Window(FormattedTextControl(text), width=88, height=24),
                            )
                        )
                    ]
                else:  # Second question
                    text = self.puzzle_messages[0] + \
                        "\n\n" + self.puzzle_messages[3] + \
                        "\n\n" + self.puzzle_messages[5] + \
                        "\n\n" + self.puzzle_messages[6]
                    self.body.floats = [
                        Float(
                            Frame(
                                Window(FormattedTextControl(text), width=88, height=24),
                            )
                        )
                    ]
                    self.puzzle_progression = 0
            elif self.active_quest == -1:  # The answer to the narrator's question after completion of the puzzle quest
                self.game_progression += 1
                self.message_box.body = Window(
                    FormattedTextControl(self.messages[self.game_progression]),
                    align=WindowAlign.CENTER
                )

        @kb.add("k")
        def quest_option_2(event: KeyPressEvent) -> None:
            if self.active_quest == 1:
                if self.puzzle_progression == 0:
                    text = self.puzzle_messages[0] + "\n\n" + self.puzzle_messages[3]
                    self.body.floats = [
                        Float(
                            Frame(
                                Window(FormattedTextControl(text), width=88, height=24),
                            )
                        )
                    ]
                    self.puzzle_progression = 1
                else:
                    text = self.puzzle_messages[0] + \
                        "\n\n" + self.puzzle_messages[3] + \
                        "\n\n" + self.puzzle_messages[4] + \
                        "\n\n" + self.puzzle_messages[6]
                    self.body.floats = [
                        Float(
                            Frame(
                                Window(FormattedTextControl(text), width=88, height=24),
                            )
                        )
                    ]
                    self.puzzle_progression = 0
                    self.completed_quests += 1
            elif self.active_quest == -1:  # The answer to the narrator's question after completion of the puzzle quest
                self.game_progression += 2
                self.message_box.body = Window(
                    FormattedTextControl(self.messages[self.game_progression]),
                    align=WindowAlign.CENTER
                )

        @kb.add("l")
        def quest_option_3(event: KeyPressEvent) -> None:
            if self.active_quest == 1:
                if self.puzzle_progression == 0:
                    text = self.puzzle_messages[0] + \
                        "\n\n" + self.puzzle_messages[2] + \
                        "\n\n" + self.puzzle_messages[6]
                    self.body.floats = [
                        Float(
                            Frame(
                                Window(FormattedTextControl(text), width=88, height=24),
                            )
                        )
                    ]
                else:
                    text = self.puzzle_messages[0] + \
                        "\n\n" + self.puzzle_messages[3] + \
                        "\n\n" + self.puzzle_messages[5] + \
                        "\n\n" + self.puzzle_messages[6]
                    self.body.floats = [
                        Float(
                            Frame(
                                Window(FormattedTextControl(text), width=88, height=24),
                            )
                        )
                    ]
                    self.puzzle_progression = 0

        # Quit mini-game
        @kb.add("q")
        def quit_minigame(event: KeyPressEvent) -> None:
            self.active_quest = -1
            self.body.floats = [
                Float(
                    Frame(
                        Window(FormattedTextControl("Quests completed: {}/3".format(self.completed_quests)),
                               width=22, height=1),
                    ),
                    right=5,
                    top=2,
                )
            ]
            self.puzzle_progression = 0

            # To be fixed, the condition should be true only just after the completion of the puzzle quest
            if self.completed_quests == 1:
                self.game_progression += 1
                self.message_box.body = Window(
                    FormattedTextControl(self.messages[self.game_progression]),
                    align=WindowAlign.CENTER
                )

        # Display the next Message
        @kb.add("n")
        def next_message(event: KeyPressEvent) -> None:
            if self.game_progression == 0:
                self.message_box.body = Window(
                    FormattedTextControl("Go find the witch hut"),
                    align=WindowAlign.CENTER
                )

        return kb

    def run(self) -> None:
        """Run the Application"""
        self.application.run()


if __name__ == "__main__":
    game = Game()
    game.run()
