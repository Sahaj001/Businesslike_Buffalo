# from numpy import unicode_
import pygments
import pygments.lexers
from prompt_toolkit.application import Application
from prompt_toolkit.formatted_text import PygmentsTokens
from prompt_toolkit.key_binding import KeyBindings, KeyPressEvent
from prompt_toolkit.layout.containers import HSplit, Window, WindowAlign
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import Frame

from entities import Bar, Fountain, Tree
from person import Person
from screen import Screen


class Game:
    """Specifies the main layout of the game i.e. the play area and the rest of the UI"""

    def __init__(self):
        """Initializes the Layout"""
        self.screen = Screen(88, 24)
        self.tree = Tree(10, 20, 5, unique_name="Tree1")
        self.player = Person(84, 20, 5, unique_name="Bob")
        self.bar = Bar(50, 3, 5, unique_name="bar1")
        self.fountian = Fountain(30, 5, 5, unique_name="fountain1")
        self.screen.insert_entity(self.tree)
        self.screen.insert_entity(self.bar)
        self.screen.insert_entity(self.fountian)
        self.screen.insert_entity(self.player, True)
        # NOTE: Temporary and will be removed later to allow for fuller narrator implementation.
        self.messages = ["Message 1", "Message 2", "Message 3", "Message 4"]
        self.current_message = 0
        self.lexer = pygments.lexers.load_lexer_from_file("highlighter.py", lexername="CustomLexer")
        self.style = Style.from_dict({
            "pygments.player": "#0000ff",
            "pygments.leaves": "#00cd00",
            "pygments.trunk": "#964B00",
            "pygments.bar": "#db9146",
            "pygments.fountainbase": "#ff7a7a",
            "pygments.water": "#0025d2",
            "pygments.wall": "#ff7a7a",
        })

        tokens = list(pygments.lex(str(self.screen.render()), lexer=self.lexer))

        self.game_field = Frame(
            body=Window(FormattedTextControl(
                text=PygmentsTokens(tokens)
            )),
            style="bg:#7cc5d9"
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

        self.application = Application(
            layout=Layout(self.container),
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
