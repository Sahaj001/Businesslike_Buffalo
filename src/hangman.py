import numpy as np


class Hangman:
    """Class for the classical hangman game."""

    def __init__(self, word: str, chance: int) -> None:
        """Initializing the word for hangman game.

        :param size: size of the word selected
        :param word: the word selected to the game
        :param chance: the number of chances left for the player to play the game
        """
        self.draw = 1
        self.word = word  # the original word
        self.size = len(word)  # length of the original word
        self.chance = chance  # number of chances for the player
        self.letter_set = self.word  # set of the letters in the original word
        self.gussed_letter_set = ""  # set of already guessed letters
        self.print_word = ""  # word with letter encoded
        for _ in self.word:
            self.print_word += '*'
        self.path = '../assets/ascii/'
        self.words = ""  # narrator's word

        with open(self.path + "hangman.txt", "r", encoding="utf8") as file:
            ascii_lst = file.read().rstrip().splitlines()

        self.height = len(ascii_lst)
        self.width = max(
            [len(line) for line in ascii_lst]
        )
        ascii_lst = [line + (self.width - len(line)) * " " for line in ascii_lst]

        self.rendered_table = np.array([list(line) for line in ascii_lst])

        with open(self.path + "hangman_body.txt", "r", encoding="utf8") as file:
            ascii_man = file.read().rstrip().splitlines()

        ascii_man = [line for line in ascii_man]
        self.man = np.array([list(line) for line in ascii_man])

    def hangman_str(self) -> str:
        """Function to return the table object as string. bot.py->print_st same docs apply here."""
        mat = ""
        for i in self.rendered_table:
            for j in i:
                mat += j
            mat += '\n'
        return mat

    def read_text(self, filename: str):
        """Reading the text file."""
        with open(filename, 'r') as file:
            data = file.read()
        return data

    def extend_hangman(self):
        """Extend the hangman drawing when the player guesses a wrong letter."""
        x = int(self.draw / 3) % 3
        y = int(self.draw % 3)
        self.draw += 1
        self.chance -= 1
        self.rendered_table[3 + x, 13 + y] = self.man[x, y]

    def input_letter(self, val: str) -> None:
        """The character that user input-ed."""
        if val in self.gussed_letter_set:
            self.words = "Letter", val, " already guessed, try a different one"

        elif val in self.letter_set:
            self.gussed_letter_set += val
            codeword = ""
            for letter in self.word:
                if letter in self.gussed_letter_set:
                    codeword += letter
                else:
                    codeword += '*'
            self.print_word = codeword
            self.words = "lucky, you guessed correctly !!"

        else:
            self.extend_hangman()
            self.words = "oops, there's no letter ", val, " in the word"

    def game_result(self) -> int:
        """Return 1 if you win the game returns 0 if you loose."""
        if self.letter_set == self.print_word:
            return 1
        else:
            return 0
