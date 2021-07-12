from pygments.lexer import RegexLexer
from pygments.token import Name

__all__ = ["CustomLexer"]


class CustomLexer(RegexLexer):
    """Highlighter for our entities."""

    name = "entity highlighter"
    tokens = {
        'root': [
            (r"[@NИ]", Name.Tag),
            (r"[│─┌┬┐└┴┘]", Name.Builtin)
        ]
    }
