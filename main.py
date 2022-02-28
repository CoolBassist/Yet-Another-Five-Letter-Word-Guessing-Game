from YAFLWGG import YAFLWGG

game = YAFLWGG()
game.new_game()
while True:
    while not game.is_game_over():
        game.print_top()
        game.parse_input(input(f"guess {game.guesses}> "))
    game.end_screen()
    game.replay()
    game.new_game()