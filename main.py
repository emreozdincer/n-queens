# Last Updated: 18 March 2018
# Author: emreozdincer

# Options
use_colors = False # If you installed Termcolor, set to True for better console output
board_size = 10 # Board size (N)
num_restarts = 10 # Number of restarts
print_iterations = True # Print resulting board states and scores during algorithm iterations

if __name__ == "__main__":
    if use_colors:
        import n_queens
    else:
        import n_queens_nocolors as n_queens

    successes = 0
    failures = 0
    for _ in range(num_restarts):
        game = n_queens.Game(board_size)

        is_successful = game.hill_climb(print_iterations)
        # is_successful = game.first_best_hill_climb(print_iterations)

        # Temperature = Temperature - Cooling Factor
        # is_successful = game.simulated_annealing(temperature=10000, cooling_factor=1, verbose=print_iterations)

        if is_successful:
            successes += 1
        else:
            failures += 1

    print ("Successes: " + str(successes) + "\nFailures: " + str(failures))
