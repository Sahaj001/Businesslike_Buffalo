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
        self.word = word
        self.size = len(word)
        self.chance = chance
        self.letter_set = set()

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

            
if __name__ == "__main__":
    
    game = Hangman("helloWorld",5)
    game.make_set()
    
    while game.chance > 0:
        print(game.chance)
        val = input("Guess the char: ")
        if isinstance(val, np.char) == False:
            print_formatted_text("please enter letter")

        elif game.letter_guessed(val) == True:
            print_formatted_text("lucky, you guessed correctly !!")

        else:
            print_formatted_text("opps, there's no letter ", val," in the word")