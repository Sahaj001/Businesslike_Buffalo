from pygments.lexer import RegexLexer
from pygments.token import Token

__all__ = ["CustomLexer"]


class CustomLexer(RegexLexer):
    """Highlighter for our entities."""

    name = "entity highlighter"
    tokens = {
        'root': [
            (r"[@NИ]", Token.Player),
            (r"(888)|(88&O8)|(8&O&&O8)", Token.Leaves),
            (r"(\)\s\()", Token.Trunk),
        ]
    }
