# Options
board_size = 5 # Board size
num_restarts = 20 # Number of restarts
verbose = True # Print board states and their scores while hill-climbing
use_colors = True # If you installed Termcolor, set to True for better output

if __name__ == "__main__":
    if use_colors:
        import n_queens
    else:
        import n_queens_nocolors as n_queens

    successes = 0
    fails = 0
    for _ in range(num_restarts):
        game = n_queens.Game(board_size)
        # success = game.hill_climb(verbose)
        success = game.first_best_hill_climb(verbose)
        if success:
            successes += 1
        else:
            fails += 1

    print ("Successes: " + str(successes) + "\nFails: " + str(fails))

    # game = n_queens.Game(board_size)
    # game.go_to_first_best_state()
