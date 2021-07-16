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

from map import Map
from person import Person
from screen import Screen


# noinspection PyTypeChecker
class Game:
    """Specifies the main layout of the game i.e. the play area and the rest of the UI"""

    def __init__(self):
        """Initializes the Layout"""
        self.screen = Screen(88, 24)
        self.player = Person(88, 20, 5, "Bob")
        screen_5 = Map()
        screen_5.map_initialise()
        [self.screen.insert_entity(entity, presence) for entity, presence in screen_5.map_1]
        self.screen.insert_entity(self.player, True)

        self.maze_trigger_coords = (54, 10)  # (x, y) of the bar door
        self.hangman_trigger_coords = (0, 0)  # (x, y) of a tree

        self.puzzle_trigger_coords = (0, 0)  # (x, y) of the fountain

        # NOTE: Temporary and will be removed later to allow for fuller narrator implementation.
        self.messages = ["Message 1", "Message 2", "Message 3", "Message 4"]

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
                         "Drink Potion\n(K) Refuse", "Good. I like the obedient Subjects", "Wrong choice!\nGame Over"]
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
            "pygments.fountain": "#ff7a7a",
            "pygments.water": "#00bafd",
            "pygments.wall.inescapable": "bg:#ed0000",
            "pygments.grass": "#9ae500",
            "pygments.campfire": "#964b00",
            "pygments.fire": "#ffe100",
            "pygments.lake": "#00d8ff",
            "pygments.tent": "#FFA200",
            "pygments.house.wall": "#AA3800",
            "pygments.house.roof": "#AAABAA"
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
                self.message_box.body = Window(
                    FormattedTextControl("Start the puzzles game"),
                    align=WindowAlign.CENTER
                )
            else:
                self.message_box.body = Window(
                    FormattedTextControl("There is nothing to do"),
                    align=WindowAlign.CENTER
                )

        # Quit mini-game
        @kb.add("q")
        def quit_minigame(event: KeyPressEvent) -> None:
            self.body.floats = [
                Float(
                    Frame(
                        Window(FormattedTextControl("Quests completed: 0/3"), width=22, height=1),
                    ),
                    right=5,
                    top=2,
                )
            ]

        # Display the next Message
        @kb.add("n")
        def next_message(event: KeyPressEvent) -> None:
            self.current_message = (self.current_message + 1) % 4
            self.message_box.body = Window(
                FormattedTextControl(self.messages[self.current_message]),
                align=WindowAlign.CENTER
            )

        return kb

    def run(self) -> None:
        """Run the Application"""
        self.application.run()


if __name__ == "__main__":
    game = Game()
    game.run()
