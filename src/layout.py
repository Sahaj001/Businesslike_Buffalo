# from numpy import unicode_
from prompt_toolkit.application import Application
from prompt_toolkit.document import Document
from prompt_toolkit.key_binding import KeyBindings, KeyPressEvent
from prompt_toolkit.layout.containers import HSplit, Window, WindowAlign
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.widgets import Frame, TextArea

from person import Person
from screen import Screen


class Game:
    """Specifies the main layout of the game i.e. the play area and the rest of the UI"""

    def __init__(self):
        """Initializes the Layout"""
        self.screen = Screen(88, 24)
        self.player = Person(20, 20, 5, unique_name="Bob")

        self.screen.insertEntity(self.player)

        # NOTE: Temporary and will be removed later to allow for fuller narrator implementation.
        self.messages = ["Message 1", "Message 2", "Message 3", "Message 4"]
        self.current_message = 0

        self.game_field = TextArea(style="class:output-field", text=self.screen.render())
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
            layout=Layout(self.container, focused_element=self.game_field),
            key_bindings=self.get_key_bindings(),
            mouse_support=True,
            full_screen=True,
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
        @kb.add("left")
        def go_left(event: KeyPressEvent) -> None:
            self.player.move('left', self.screen.getCurrentScreen())
            self.screen.updateEntity(self.player)
            # TEMPORARY
            self.screen.screens[self.screen.current_screen].render_screen()

            new_text = self.screen.render()

            self.game_field.buffer.document = Document(
                text=new_text, cursor_position=len(new_text)
            )

        @kb.add("right")
        def go_right(event: KeyPressEvent) -> None:
            self.player.move('right', self.screen.getCurrentScreen())
            self.screen.updateEntity(self.player)
            # TEMPORARY
            self.screen.screens[self.screen.current_screen].render_screen()

            new_text = self.screen.render()

            self.game_field.buffer.document = Document(
                text=new_text, cursor_position=len(new_text)
            )

        @kb.add("up")
        def go_up(event: KeyPressEvent) -> None:
            self.player.move('up', self.screen.getCurrentScreen())
            self.screen.updateEntity(self.player)
            # TEMPORARY
            self.screen.screens[self.screen.current_screen].render_screen()

            new_text = self.screen.render()

            self.game_field.buffer.document = Document(
                text=new_text, cursor_position=len(new_text)
            )

        @kb.add("down")
        def go_down(event: KeyPressEvent) -> None:
            self.player.move('down', self.screen.getCurrentScreen())
            self.screen.updateEntity(self.player)
            # TEMPORARY
            self.screen.screens[self.screen.current_screen].render_screen()

            new_text = self.screen.render()

            self.game_field.buffer.document = Document(
                text=new_text, cursor_position=len(new_text)
            )

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
