from pygments.lexer import RegexLexer
from pygments.token import Token


class CustomLexer(RegexLexer):
    """Highlighter for our entities."""

    name = "entity highlighter"
    tokens = {
        'root': [
            (r"[@NИ]", Token.Player),
            (r"8*(&|0|8)", Token.Leaves),
            (r"(\).*?\()", Token.Trunk),
            (r"(║.*?║)|([╠═╔══╗═╣])", Token.Bar),
            (r"[░]", Token.Water),
            (r"(/_\|_\\)|(/__\|__\\)|(v)", Token.Fountain),
            (r"\%*\%", Token.Wall.Inescapable),
            (r",", Token.Grass),
            (r"/\|\\", Token.Campfire),
            (r"\*", Token.Fire),
            (r"(\\|/)[~_@NИ]+(\\|/)|(_)", Token.Lake),
            (r"(/\\)|(//\\\\)|(\\/)", Token.Tent),
            # (r"|.*?|", Token.House.Wall),
            # (r"*_[\s]", Token.House.Roof),
        ]
    }
