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
        self.word = word
        self.size = len(word)
        self.chance = chance
        self.letter_set = set()
        self.path = '/Users/sahajsingh/Desktop/python_code_jam/Businesslike_Buffalo/assets/ascii/'
        
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
        
    def to_str(self):
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

    def make_set(self)->set():
        for i in self.word:
            self.letter_set.add(i)

    def letter_guessed(self, letter) -> bool:
        self.chance = self.chance - 1
        for i in self.letter_set:
            if i == letter:
                self.letter_set.remove(letter)
                return True
        return False
    
    def draw_hangman(self):
        x = int(self.draw/3)%3
        y = int(self.draw%3)
        self.draw += 1
        print(x, " ", y)
        self.rendered_table[3+x, 13+y] = self.man[x, y]
        print(self.to_str())

            
if __name__ == "__main__":
    
    game = Hangman("helloWorld",9)
    game.make_set()
    print(game.man)
    while game.chance > 0:
        print(game.chance)
        val = input("Guess the char: ")
        if game.letter_guessed(val) == True:
            print_formatted_text("lucky, you guessed correctly !!")

        else:
            game.draw_hangman()
            print_formatted_text("opps, there's no letter ", val," in the word")
            
    if game.chance == 0:
        print("You Lost the Game, Better Luck Next time gussinng.")