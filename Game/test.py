import random
import time

import grid
import person
import pygments.lexers
from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import PygmentsTokens
from prompt_toolkit.styles import Style

lexer = pygments.lexers.load_lexer_from_file("regex.py", lexername='CustomLexer')

if __name__ == "__main__":
    p = person.Person(5, 5, 1)
    plane1 = grid.Grid(12, 12)
    plane1.insert_entity(p)
    plane1.insert(0, 0, ["┌"])
    plane1.insert(0, 11, ["└"])
    for plane1_x in range(1, 11):
        plane1.insert(plane1_x, 0, ["─"])
        plane1.insert(plane1_x, 11, ["─"])
    plane1.insert(11, 0, ["┐"])
    plane1.insert(11, 11, ["┘"])

    for plane1_y in range(1, 11):
        plane1.insert(0, plane1_y, ["│"])
        plane1.insert(11, plane1_y, ["│"])

    style = Style.from_dict({
        'pygments.name.tag': '#0000ff',
        'pygments.name.builtin': 'bg:#edaaaa',
    })

    while True:
        tokens = list(pygments.lex(str(plane1), lexer=lexer))
        # os.system('clear') if sys is windows then do os.system('cls') also import os at the start : )
        user_response = random.choice(['right', 'left', 'up', 'down'])
        print(user_response)
        p.move(user_response, plane1)
        plane1.update_entity(p, p.old_x, p.old_y)
        print_formatted_text(PygmentsTokens(tokens), style=style)
        time.sleep(1)
