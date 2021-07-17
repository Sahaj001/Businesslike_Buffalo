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
from quests import Quest
from screen import Screen


# noinspection PyTypeChecker
class Game:
    """Specifies the main layout of the game i.e. the play area and the rest of the UI"""

    def __init__(self):
        """Initializes the Layout"""
        self.screen = Screen(88, 24)
        self.player = Person(88, 20, 5, "Bob")
        mp = Map()
        mp.map_initialise()
        [self.screen.insert_entity(entity, presence, screen) for entity, presence, screen in mp.map_1]
        [self.screen.insert_entity(entity, presence, screen) for entity, presence, screen in mp.map_2]
        [self.screen.insert_entity(entity, presence, screen) for entity, presence, screen in mp.map_3]
        self.screen.insert_entity(self.player, True)

        self.maze_trigger_coords = (24, 17)  # (x, y) of the bar door
        self.hangman_trigger_coords = (59, 17)  # (x, y) of a tree
        self.puzzle_trigger_coords = (64, 16)  # (x, y) of the fountain

        self.can_walk = True
        self.current_quest = 1
        self.quests_generator = Quest()

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
                FormattedTextControl(self.quests_generator.get_message(self.current_quest, 0)),
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
            if self.can_walk:
                self.player.move('left', self.screen.get_current_screen())
                self.screen.update_entity(self.player, True)

                new_text = self.screen.render()
                tokens = list(pygments.lex(new_text, lexer=self.lexer))

                self.game_field.body = Window(
                    FormattedTextControl(
                        text=PygmentsTokens(tokens)
                    ))
            elif self.current_quest == 4:
                self.body.floats = [
                    Float(
                        Frame(
                            Window(FormattedTextControl(self.quests_generator.get_message(
                                self.current_quest, -1, "a")), width=88, height=24),
                        )
                    )
                ]

        @kb.add("d")
        @kb.add("right")
        def go_right(event: KeyPressEvent) -> None:
            if self.can_walk:
                self.player.move('right', self.screen.get_current_screen())
                self.screen.update_entity(self.player, True)

                new_text = self.screen.render()
                tokens = list(pygments.lex(new_text, lexer=self.lexer))

                self.game_field.body = Window(
                    FormattedTextControl(
                        text=PygmentsTokens(tokens)
                    ))
            elif self.current_quest == 4:
                self.body.floats = [
                    Float(
                        Frame(
                            Window(FormattedTextControl(self.quests_generator.get_message(
                                self.current_quest, -1, "d")), width=88, height=24),
                        )
                    )
                ]

        @kb.add("w")
        @kb.add("up")
        def go_up(event: KeyPressEvent) -> None:
            if self.can_walk:
                self.player.move('up', self.screen.get_current_screen())
                self.screen.update_entity(self.player, True)

                new_text = self.screen.render()
                tokens = list(pygments.lex(new_text, lexer=self.lexer))

                self.game_field.body = Window(
                    FormattedTextControl(
                        text=PygmentsTokens(tokens)
                    ))
            elif self.current_quest == 4:
                self.body.floats = [
                    Float(
                        Frame(
                            Window(FormattedTextControl(self.quests_generator.get_message(
                                self.current_quest, -1, "w")), width=88, height=24),
                        )
                    )
                ]

        @kb.add("s")
        @kb.add("down")
        def go_down(event: KeyPressEvent) -> None:
            if self.can_walk:
                self.player.move('down', self.screen.get_current_screen())
                self.screen.update_entity(self.player, True)

                new_text = self.screen.render()
                tokens = list(pygments.lex(new_text, lexer=self.lexer))

                self.game_field.body = Window(
                    FormattedTextControl(
                        text=PygmentsTokens(tokens)
                    ))
            elif self.current_quest == 4:
                self.body.floats = [
                    Float(
                        Frame(
                            Window(FormattedTextControl(self.quests_generator.get_message(
                                self.current_quest, -1, "s")), width=88, height=24),
                        )
                    )
                ]

        # Action Key
        @kb.add("x")
        def action(event: KeyPressEvent) -> None:
            if (self.player.x, self.player.y) == self.maze_trigger_coords:

                self.body.floats = [
                    Float(
                        Frame(
                            Window(FormattedTextControl(self.quests_generator.get_message(self.current_quest, 0)),
                                   width=88, height=24),
                        )
                    )
                ]
                self.can_walk = False
            elif (self.player.x, self.player.y) == self.hangman_trigger_coords:
                self.body.floats = [
                    Float(
                        Frame(
                            Window(FormattedTextControl(self.quests_generator.get_message(self.current_quest, 0)),
                                   width=88, height=24),
                        )
                    )
                ]
                self.can_walk = False
            elif (self.player.x, self.player.y) == self.puzzle_trigger_coords:
                self.body.floats = [
                    Float(
                        Frame(
                            Window(FormattedTextControl(self.quests_generator.get_message(self.current_quest, 0)),
                                   width=88, height=24),
                        )
                    )
                ]
                self.can_walk = False
            #  else:
            #      self.message_box.body = Window(
            #          FormattedTextControl(str(self.player.x) + str(self.player.y)),
            #          align=WindowAlign.CENTER
            #      )

        @kb.add("j")
        def option1(event: KeyPressEvent) -> None:
            if not self.can_walk:
                self.body.floats = [
                    Float(
                        Frame(
                            Window(FormattedTextControl(self.quests_generator.get_message(
                                self.current_quest, 1)), width=88, height=24),
                        )
                    )
                ]
            else:
                self.message_box.body = Window(
                    FormattedTextControl(self.quests_generator.get_message(self.current_quest, 1)),
                    align=WindowAlign.CENTER
                )

        @kb.add("k")
        def option2(event: KeyPressEvent) -> None:
            if not self.can_walk:
                self.body.floats = [
                    Float(
                        Frame(
                            Window(FormattedTextControl(self.quests_generator.get_message(
                                self.current_quest, 2)), width=88, height=24),
                        )
                    )
                ]
            else:
                self.message_box.body = Window(
                    FormattedTextControl(self.quests_generator.get_message(self.current_quest, 2)),
                    align=WindowAlign.CENTER
                )

        @kb.add("l")
        def option3(event: KeyPressEvent) -> None:
            if not self.can_walk:
                self.body.floats = [
                    Float(
                        Frame(
                            Window(FormattedTextControl(self.quests_generator.get_message(
                                self.current_quest, 3)), width=88, height=24),
                        )
                    )
                ]

        @kb.add("<any>")
        def alphabets(event: KeyPressEvent) -> None:
            if event.key_sequence[0].key.isalpha():
                if not self.quests_generator.is_complete(self.current_quest):
                    self.body.floats = [
                        Float(
                            Frame(
                                Window(FormattedTextControl(
                                       self.quests_generator.get_message(self.current_quest,
                                                                         0,
                                                                         event.key_sequence[0].key)
                                       ),
                                       width=88,
                                       height=24),
                            )
                        )
                    ]
                else:
                    self.body.floats = [
                        Float(
                            Frame(
                                Window(FormattedTextControl("Press 'q'"),
                                       width=88,
                                       height=24),
                            )
                        )
                    ]
                    self.current_quest += 1

        # Quit mini-game
        @kb.add("q")
        def quit_minigame(event: KeyPressEvent) -> None:
            self.message_box.body = Window(
                FormattedTextControl(self.quests_generator.get_message(self.current_quest, -2)),
                align=WindowAlign.CENTER
            )
            if self.quests_generator.is_complete(self.current_quest):
                self.current_quest += 1
            self.body.floats = [
                Float(
                    Frame(
                        Window(FormattedTextControl("Quests completed: {}/3".format(self.current_quest - 1)),
                               width=22, height=1),
                    ),
                    right=5,
                    top=2,
                )
            ]
            self.can_walk = True

        # Display the next Message
        @kb.add("n")
        def next_message(event: KeyPressEvent) -> None:
            if self.quests_generator.is_complete(self.current_quest):
                self.current_quest += 1
                self.body.floats = [
                    Float(
                        Frame(
                            Window(FormattedTextControl("Quests completed: {}/3".format(self.current_quest - 1)),
                                   width=22, height=1),
                        ),
                        right=5,
                        top=2,
                    )
                ]
                self.message_box.body = Window(
                    FormattedTextControl(self.quests_generator.get_message(self.current_quest, -1)),
                    align=WindowAlign.CENTER
                )
            else:
                self.message_box.body = Window(
                    FormattedTextControl(self.quests_generator.get_message(self.current_quest, -1)),
                    align=WindowAlign.CENTER
                )

        return kb

    def run(self) -> None:
        """Run the Application"""
        self.application.run()


if __name__ == "__main__":
    game = Game()
    game.run()
