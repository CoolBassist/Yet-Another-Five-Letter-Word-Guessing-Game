import random
from rich.console import Console
import wordlist

class YAFLWGG:
    def __init__(self, mode="regular"):
        self.win = False
        self.current_word = ["-"]*5
        self.jumbled_letters = []
        self.guessed_words = []
        self.guesses = 1
        self.console = Console()
        self.message = ""
        if mode == "regular":
            self.wordlist = wordlist.regular
        elif mode == "hard":
            self.wordlist = wordlist.hard
        else:
            self.console.print("[white on red]Wordlist not recoginisable: " + mode + "[/white on red]")
            exit()
        
    def get_new_word(self):
        self.word = self.wordlist[random.randint(0, len(self.wordlist)-1)]
        self.guesses = 1
        self.alphabet = dict()
        for i in range(97, 123):
            self.alphabet[chr(i)] = 0
        self.qwerty = list("qwertyuiopasdfghjklzxcvbnm")
        
        return self.word

    def guess(self, word_guess):
        self.message = ""
        correct_letters = ["-", "-", "-", "-", "-"]
        almost_letters = []
        wrong_letters = []

        word_guess = word_guess.lower()
        
        if len(word_guess) != 5:
            self.message = "Please enter a five letter word"
            return
        if word_guess == self.word:
            self.win = True
            return
        if word_guess not in self.wordlist:
            self.message = "Word not in word list"  
            return
            

        guessed = [i for i in word_guess]
        guessed_letters = []
        
        #correct letter pass
        for char in range(len(word_guess)):
            if  word_guess[char] == self.word[char]:
                guessed[char] = "[bold green]" + word_guess[char] + "[/bold green]"
                if self.alphabet[word_guess[char]] in [0, 2]:
                    self.alphabet[word_guess[char]] = 1
                guessed_letters.append(word_guess[char])
                correct_letters[char] = word_guess[char]

        #almost letter pass
        for char in range(len(word_guess)):
            if len(guessed[char]) != 1:
                continue
            if word_guess[char] in self.word and (guessed_letters.count(word_guess[char]) < self.word.count(word_guess[char])):
                guessed[char] = "[bold red]" + word_guess[char] + "[/bold red]"
                if self.alphabet[word_guess[char]] == 0:
                    self.alphabet[word_guess[char]] = 2
                guessed_letters.append(word_guess[char])
                almost_letters.append(word_guess[char])
        
        for letter in word_guess:
            #if letter not in correct_letters and letter not in almost_letters:
            if letter not in self.word:
                wrong_letters.append(letter)
                if self.alphabet[letter] == 0:
                    self.alphabet[letter] = 3
        
        actual_print = "".join([i for i in guessed])

        self.guessed_words.append(actual_print)

        self.guesses += 1

        return (correct_letters, almost_letters, wrong_letters)

    def has_won(self):
        return self.win

    def print_words(self):
        for i in range(len(self.guessed_words)):
            print(f"guess {i+1}> ", end="")
            self.console.print(self.guessed_words[i])
    
    def print_alphabet(self):
        current_row = "[center]"
        for i in self.qwerty:
            if i in ['a', 'z']:
                current_row += "\n"
            if self.alphabet[i] == 1:
                current_row += "[bold green]" + i + "[/bold green] "
            if self.alphabet[i] == 2:
                current_row += "[bold red]" + i + "[/bold red] "
            if self.alphabet[i] == 3:
                current_row += "[bold black]" + i + "[/bold black] "
            if self.alphabet[i] == 0:
                current_row += i + " "
        self.console.print(current_row + "[/center]", justify="center")
