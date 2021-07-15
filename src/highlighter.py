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
            (r"[v/-_|\\]", Token.Fountainbase),
            (r"\%*\%", Token.Wall.Inescapable),
        ]
    }
