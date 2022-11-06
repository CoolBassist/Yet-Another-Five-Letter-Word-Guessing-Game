from email import message
from random import randint
from rich.console import Console
from rich.prompt import Prompt
from typing import List
import os
import sys

class YAFLWGG:
    def __init__(self, mode="regular"):
        self.console = Console()
        self.message = ""
        self.streak = 0
        self.qwerty = list("qwertyuiopasdfghjklzxcvbnm")
        self.full_word_list = self.load_full_w_list()
        self.word_list = self.load_word_list(mode)
    
    def load_full_w_list(self) -> List[str]:
        from wordLists import F_wordlist
        return F_wordlist[:]
    
    def load_word_list(self, mode: str) -> List[str]:
        if mode == "regular":
            from wordLists import R_wordlist
            return R_wordlist[:]
        else:
            self.log("Unrecoginised word list:" + mode, "white on red")
    
    def new_game(self) -> None:
        self.win = False
        self.guessed_words = []
        self.game_over = False
        self.word = self.word_list[randint(0, len(self.word_list)-1)]
        self.guesses = 1
        self.alphabet = dict()
        for i in range(97, 123):
            self.alphabet[chr(i)] = 0

    def print_top(self) -> None:
        if sys.platform.startswith('win'):
            os.system("cls")
        else:
            os.system("clear")
        self.print_title_rules()
        self.print_streak()
        if len(self.message) != 0:
            self.console.print("[white on red]" + self.message + "[/white on red]", justify="center")
        else:
            print("")
        self.print_alphabet()
        self.print_prev_words()

    def print_title_rules(self) -> None:
        self.console.print("""╔═════════════════════╗
║ Welcome to [bold u magenta]YAFLWGG[/bold u magenta]! ║
╚═════════════════════╝""", justify="center")
        self.console.print("[u]Rules[/u]:", justify="center", style="bold")
        self.console.print("Guess the [b]word[/b] in 6 tries.", justify="center")
        self.console.print("[green]w[/green]eary\nThe letter [b]w[/b] is in the word, and in the correct spot.", justify="center")
        self.console.print("pi[red]l[/red]ot\nThe letter [b]l[/b] is in the word, but in the wrong spot.", justify="center", style="white")
        self.console.print("[white]vague\nNone of these letters are in the word.[/white]", justify="center")

    def print_streak(self) -> None:
        self.console.print(f"\n\nCurrent Streak: {self.streak}", justify="center")

    def print_alphabet(self) -> None:
        current_row = ""
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
        self.console.print(current_row, justify="center")

    def print_prev_words(self) -> None:
        for i in range(len(self.guessed_words)):
            print(f"guess {i+1}> ", end="")
            self.console.print(self.guessed_words[i])

    def parse_input(self, input: str) -> None:
        input = input.strip(" \t")
        self.message = ""
        if self.guesses >= 6:
            self.game_over = True
        if len(input) == 0:
            self.message = "Hey man you cant leave the input empty!"
            return
        if input[0] == "!":
            self.parse_command(input)
        else:
            if len(input) != 5:
                self.message = "Please enter a five letter word!"
            elif input not in self.full_word_list:
                self.message = "Word not in word list!"
            else:
                self.guess(input)

    def guess(self, word_guess: str) -> None:
        correct_letters = ["-", "-", "-", "-", "-"]
        almost_letters = []
        wrong_letters = []

        word_guess = word_guess.lower()
        if word_guess == self.word:
            self.win = True
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

    def log(self, message, style:str="b") -> None:
        message = str(message)
        self.console.print("[" + style + "]" + message)

    def has_won(self) -> None:
        return self.win
    
    def is_game_over(self) -> None:
        return self.win or self.game_over

    def end_screen(self) -> None:
        if self.win:
            self.streak += 1
            self.log(f"[green]You won![/green] You have increased your score to {self.streak}!")
        else:
            self.log(f"[red]You lost![/red] You lost your streak of {self.streak}!\nThe word was {self.word}!")
            self.streak = 0
    
    def replay(self) -> None:
        start_again = Prompt.ask("Do you want to play again?", choices=["yes", "no"])
        if start_again == "no":
            self.log("Good bye!", "white on blue")
            exit()
    
    