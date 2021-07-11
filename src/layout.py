from prompt_toolkit.application import Application
from prompt_toolkit.document import Document
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, Window, WindowAlign
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.widgets import TextArea, Frame
from prompt_toolkit.layout.controls import FormattedTextControl


class Game:
    """
    Specifies the main layout of the game
    i.e. the play area and the rest of the UI
    """

    def __init__(self):
        """Initializes the Layout"""

        # TODO: get the text from "Screen" Object
        self.text = """
        The main game goes here
        """

        # TODO: Add the typing animation and come up with a neater approach to import/store the messages
        self.messages = ["Message 1", "Message 2", "Message 3", "Message 4"]
        self.current_message = 0

        self.game_field = TextArea(style="class:output-field", text=self.text)
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

    def get_key_bindings(self):
        """Add different key bindings to control the player/UI
        :return: KeyBindings Object
        """
        kb = KeyBindings()

        # Exit
        @kb.add("c-c")
        @kb.add("c-q")
        def _(event):
            "Pressing Ctrl-Q or Ctrl-C will exit the user interface."
            event.app.exit()

        # Movement
        @kb.add("left")
        def go_left(event):
            new_text = self.text + "\nLeft Pressed"
            self.game_field.buffer.document = Document(
                text=new_text, cursor_position=len(new_text)
            )

        @kb.add("right")
        def go_right(event):
            new_text = self.text + "\nRight Pressed"
            self.game_field.buffer.document = Document(
                text=new_text, cursor_position=len(new_text)
            )

        @kb.add("up")
        def go_up(event):
            new_text = self.text + "\nUp Pressed"
            self.game_field.buffer.document = Document(
                text=new_text, cursor_position=len(new_text)
            )

        @kb.add("down")
        def go_down(event):
            new_text = self.text + "\nDown Pressed"
            self.game_field.buffer.document = Document(
                text=new_text, cursor_position=len(new_text)
            )

        # Display the next Message
        @kb.add("n")
        def next_message(event):
            self.current_message = (self.current_message + 1) % 4
            self.message_box.body = Window(
                FormattedTextControl(self.messages[self.current_message]),
                align=WindowAlign.CENTER
            )

        return kb

    def run(self):
        """Run the Application"""
        self.application.run()


if __name__ == "__main__":
    Game().run()
