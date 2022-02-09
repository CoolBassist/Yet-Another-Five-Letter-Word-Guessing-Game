from words import Wordle
from rich import print
from rich.console import Console
import os
import sys

game = Wordle()
console = Console()

streak = 0

while True:
	if "win" in sys.platform:
		os.system("cls")
	else:
		os.system("clear")

	console.print("""╔═════════════════════╗	
║ Welcome to [bold u magenta]YAFLWGG[/bold u magenta]! ║
╚═════════════════════╝""", justify="center")

	console.print("[u]Rules[/u]:", justify="center", style="bold")
	console.print("Guess the [b]word[b] in 6 tries.", justify="center")
	console.print("[green]w[/green]eary\nThe letter [b]w[b] is in the word, and in the correct spot.", justify="center")
	console.print("pi[red]l[/red]ot\nThe letter [b]l[b] is in the word, but in the wrong spot.", justify="center", style="white")
	console.print("[white]vague\nNone of these letters are in the word.[/white]", justify="center")
	console.print(f"\n\nCurrent Streak: {streak}", justify="center")

	word = game.get_new_word()
	#print(game.word)

	while not game.has_won() and game.guesses != 7:
		print(game.new_guess(input(f"guess {game.guesses}> ")))

	if game.has_won():
		print("[bold green]You won![/bold green]")
		streak += 1
		print(f"Your streak is {streak}!")
	else:
		print("[bold red]You lost![/bold red]")
		print("The word was [bold magenta]" + game.word + "[/bold magenta]")
		print(f"You have lost your {streak} streak!")
		streak = 0
		
	while (inp := input("Do you want to play again? ")) not in ["yes", "no"]:
		print("Please enter yes or no")
	
	if inp == "no":
		exit()
	else:
		game = Wordle()
		continue
	