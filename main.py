# Options
n = 10 # Board size
num_restarts = 10 # Number of restarts
use_colors = True # If you installed Termcolor, set to True for better output

if __name__ == "__main__":
    if use_colors:
        import n_queens
    else:
        import n_queens_nocolors as n_queens

    successes = 0
    fails = 0
    for _ in range(num_restarts):
        game = n_queens.Game(n)
        success = game.hill_climb(verbose = True)
        if success:
            successes += 1
        else:
            fails += 1

    print ("Successes: " + str(successes) + "\nFails: " + str(fails))
