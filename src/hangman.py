from ctypes import sizeof
import numpy as np
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts.utils import print_formatted_text

class Hangman:
    """
    class for the classical hangman game
    """
    def __init__(self, word: str, chance: int) -> None:
        """
        class for hangman game
        :param size: size of the word selected
        :param word: the word selected to the game
        :param chance: the number of chances left for the player to play the game
        """
        self.draw = 1
        self.word = word        # the original word
        self.size = len(word)   # length of the original word
        self.chance = chance    # number of chances for the player
        self.letter_set = self.word # set of the letters in the orignal word
        self.gussed_letter_set = ""  # set of already gussed letters
        self.print_word = "" # word with letter encoded
        for i in self.word:
            self.print_word += '*'
        self.path = '../assets/ascii/'
        self.words = ""     # narrator's word

        with open(self.path+ "hangman.txt", "r", encoding="utf8") as file:
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

    def hangman_str(self):
        """ Function to return the table object as string"""
        mat = ""
        for i in self.rendered_table:
            for j in i:
                mat += j
            mat += '\n'
        return mat

    def read_text(self, filename: str):
        """ reading the text file """
        with open(filename, 'r') as file:
            data = file.read()
        return data

    def extend_hangman(self):
        """
        Extend the hangman drawing when the player gusses a wrong letter
        """
        x = int(self.draw/3)%3
        y = int(self.draw%3)
        self.draw += 1
        self.chance -= 1
        #  print(x, " ", y)
        self.rendered_table[3+x, 13+y] = self.man[x, y]

    def input_letter(self, val):
        if val in self.gussed_letter_set:
            self.words = "Letter", val, " already guessed, try a different one"

        elif val in self.letter_set:
            self.gussed_letter_set += val
            codeword = ""
            for i in self.word:
                if i in self.gussed_letter_set:
                    codeword += i
                else:
                    codeword += '*'
            self.print_word = codeword
            self.words = "lucky, you guessed correctly !!"

        else:
            self.extend_hangman()
            self.words = "opps, there's no letter ", val ," in the word"

    def game_result(self):
        #  print(len(self.letter_set))
        if self.letter_set == self.print_word:
            return 1
        else:
            return 0


if __name__ == "__main__":

    game = Hangman("helloWorld",9)

    while game.chance > 0:
        print("\n\n\t\t ######### Number of chances left : ", game.chance)
        val = input("Guess the char: ")
        game.input_letter(val)
        print(game.hangman_str())
        print("the decoded letters are: ", game.print_word)
        print(game.words)

    print(game.game_result())

