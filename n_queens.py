# Last Updated: 18 March 2018
# Author: emreozdincer

from termcolor import colored
from collections import Counter
from math import factorial, exp, pow
import random
import copy

# from time import sleep
# import pdb # Debug

DEBUG = False
# Print function for DEBUG = True
def log(s):
    if DEBUG:
        print s

# Calculates C(n,r)
def combination(n,r, verbose = False):
    f = factorial
    result = f(n) / f(r) / f(n-r)
    if verbose:
        print("C(n,r) = " + str(result))
    return result

class Game:
    def __init__(self, n):
        # Initialize a game board with n elements.
        self.board = Board(n)
        print ("Game initialized with size " + str(n) + ".")

        # Initialize n queens, and place them on the board column by column
        self.queens = [None] * n
        for column in range(n):
            row = random.randint(0,n-1);
            self.queens[column] = Queen(row, column)
            self.board.update_element(self.queens[column], row, column)

        log (str(n) + " queens are randomly placed on board.")
        log (self.board)

    # Updates current game state to a new state
    def update_to_state(self, next_state):
        self.board = next_state.board
        self.queens = next_state.queens

    # Moves a queen to new_row in game board
    def move_queen(self, new_row, queen, verbose = False):
        update_text = colored("\nQueen " + str(queen.id) + " to row " + str(new_row) + "!", 'green')
        old_row = queen.row
        self.board.update_element(0, old_row, queen.col)
        self.board.update_element(queen, new_row, queen.col)
        queen.update_row(new_row) # not sure if this line is important
        self.queens[queen.col].update_row(new_row)

        if (verbose):
            print ("Queen's old row: " + str(old_row))
            print ("Queen's new row: " + str(new_row))
            print(update_text)
            print(self.board)

    # Hill Climbing algorithm
    # Returns True if finds global minimum, False otherwise
    def hill_climb(self, verbose = True):
        best_state_found = False
        iteration_count = 0
        while (best_state_found == False and self.board.current_score != 0):
            iteration_count += 1
            best_state_found = self.go_to_next_best_state()

            if verbose:
                print (colored("\nIteration " + str(iteration_count),'yellow'))
                print (self.board)
                print ("Current score: " + str(self.board.current_score))

        print ('Hit local minimum with score: ' + str(self.board.current_score))

        if (self.board.current_score == 0):
            print (colored('Success!', 'green'))
            return True
        else:
            print (colored('Fail!','red'))
            return False

    # First Best Hill Climbing algorithm
    # Returns True if finds global minimum, False otherwise
    def first_best_hill_climb(self, verbose = True):
        better_state_exists = True
        iteration_count = 0
        while (better_state_exists == True and self.board.current_score != 0):
            iteration_count += 1
            better_state_exists = self.go_to_first_best_state()

            if verbose:
                print (colored("\nIteration " + str(iteration_count),'yellow'))
                print (self.board)
                print ("Current score: " + str(self.board.current_score))
                # sleep(0.2)

        print ('Hit local minimum with score: ' + str(self.board.current_score))

        if (self.board.current_score == 0):
            print (colored('Success!', 'green'))
            return True
        else:
            print (colored('Fail!','red'))
            return False

    # Simulated Annealing algorithm
    # Temperature decreases by cooling factor in each round
    # Returns True if finds global minimum, False otherwise
    def simulated_annealing(self, temperature = 10000, cooling_factor = 50, verbose = True):
        iteration_count = 0
        while (temperature > 0 and self.board.current_score != 0):
            iteration_count += 1

            self.simulated_annealing_next_node(temperature)

            if verbose:
                print (colored("\nIteration " + str(iteration_count),'yellow'))
                print ('Temperature: ' + str(temperature))
                print (self.board)
                print ("Current score: " + str(self.board.current_score))
                # sleep(0.2)

            temperature -= cooling_factor

        print ('Simulated Annealing result: ' + str(self.board.current_score))

        if (self.board.current_score == 0):
            print (colored('Success!', 'green'))
            return True
        else:
            print (colored('Fail!','red'))
            return False

    # Goes to chosen state
    def simulated_annealing_next_node(self, temperature):
        log("Initial score: " + str(self.board.current_score))

        n = self.board.size_n
        resulting_state = copy.deepcopy(self)
        queens = copy.deepcopy(self.queens)
        current_best_score = self.board.current_score
        chose_state = False

        # Calculate scores for every available next state
        # For each queen (randomized)
        random.shuffle(queens)
        for queen in queens:
            # Break loop if we chose a state
            if chose_state:
                break

            # There exists n-1 rows to explore
            rows_to_explore = [x for x in range(n)]
            rows_to_explore.pop(queen.row)

            # For each unexplored row(randomized):
            random.shuffle(rows_to_explore)
            for row in rows_to_explore:
                queens_original_row = queen.row
                next_state = copy.deepcopy(self)
                next_state.move_queen(row, queen)

                if (next_state.board.current_score == 0):
                    chose_state = True
                    resulting_state = next_state
                    break

                delta_e = next_state.board.current_score - current_best_score
                if (delta_e > 0):
                    # choose this state
                    chose_state = True
                    resulting_state = next_state
                    break
                else:
                    # with probability e^(dE/T)
                    probability = float(delta_e)/temperature
                    if (random.random() < exp(probability)):
                        #choose this state
                        chose_state = True
                        resulting_state = next_state
                        break
                        # Put the explorer queen back to original place
                    else:
                        queen.update_row(queens_original_row)

        self.update_to_state(resulting_state)
        log("Iteration score: " + str(self.board.current_score))

    # Goes to next best state, returns boolean best_state_found
    def go_to_next_best_state(self):
        log("Initial score: " + str(self.board.current_score))

        n = self.board.size_n
        queens = copy.deepcopy(self.queens)
        best_state = copy.deepcopy(self)
        best_score = self.board.current_score
        best_state_found = True # assume true, set to false if appropriate

        # Calculate scores for every available next state
        # For each queen
        for queen in queens:
            # There exists n-1 rows to explore
            rows_to_explore = [x for x in range(n)]
            rows_to_explore.pop(queen.row)

            # For each unexplored row:
            for row in rows_to_explore:
                queens_original_row = queen.row
                next_state = copy.deepcopy(self)
                next_state.move_queen(row, queen)
                # If moving the queen yields a better result than the current state
                # Save the next best state
                if (next_state.board.current_score < best_score):
                    best_state_found = False
                    best_state = next_state
                    best_score = next_state.board.current_score
                # Put the explorer queen back to original place
                else:
                    queen.update_row(queens_original_row)

        self.update_to_state(best_state)
        log("Best iteration score: " + str(self.board.current_score))
        return best_state_found

    # Goes to first best state if possible, returns boolean first_best_state_found
    def go_to_first_best_state(self):
        log("Initial score: " + str(self.board.current_score))

        n = self.board.size_n
        queens = copy.deepcopy(self.queens)
        first_best_state = copy.deepcopy(self)
        first_best_state_found = False
        first_best_score = self.board.current_score

        # Calculate scores for every available next state
        # For each queen (randomized)
        random.shuffle(queens)
        for queen in queens:
            # Break loop if we found a better state
            if first_best_state_found:
                break

            # There exists n-1 rows to explore
            rows_to_explore = [x for x in range(n)]
            rows_to_explore.pop(queen.row)

            # For each unexplored row(randomized):
            random.shuffle(rows_to_explore)
            for row in rows_to_explore:
                queens_original_row = queen.row
                next_state = copy.deepcopy(self)
                next_state.move_queen(row, queen)
                # If moving the queen yields a better result than the current state
                # Save the next best state
                if (next_state.board.current_score < first_best_score):
                    log("First better state is found with score " + str(next_state.board.current_score))
                    first_best_state_found = True
                    first_best_state = next_state
                    break
                # Put the explorer queen back to original place
                else:
                    queen.update_row(queens_original_row)

        self.update_to_state(first_best_state)
        log("First Best State's score: " + str(self.board.current_score))
        return first_best_state_found

class Board:
    # Initializes empty n x n board
    def __init__(self, n):
        self.board = [[0]*n for x in range(n)]
        self.size_n = n
        self.current_score = 9999

    # Represent the class object as its board
    def __repr__(self):
        # return ('B')
        return ('\n'.join(map(repr, self.board)))

    def update_element(self, element, row, col):
        self.board[row][col] = element
        self.calculate_score()

    def get_current_score(self):
        return self.current_score

    # Calculates each score for current board state
    def calculate_score(self, check_vertical_conflicts = False, verbose = False):
        n = self.size_n
        score = 0
        # Check horizontal conflicts
        # For each row, count the number of queens, save in 'queens_by_rows' array
        queens_by_rows = [0] * n
        horizontal_conflicts = 0
        for row in range(n):
            for column in range(n):
                if (isinstance(self.board[row][column], Queen)):
                    queens_by_rows[row] += 1
            if (queens_by_rows[row] >= 2):
                horizontal_conflicts += combination(queens_by_rows[row],2)

        # Check vertical conflicts
        # For each column, count the number of queens, save in 'queens_by_columns' array
        if check_vertical_conflicts == False:
            pass
        else:
            queens_by_columns = [0] * n
            for column in range(n):
                for row in range(n):
                    if (isinstance(self.board[row][column], Queen)):
                        queens_by_columns[column] += 1

        # Check diagonal conflicts
        f_diagonal_conflicts, b_diagonal_conflicts = self.get_diagonal_conflicts()
        score = horizontal_conflicts + f_diagonal_conflicts + b_diagonal_conflicts
        if (verbose):
            log ("horizontal_conflicts: " + str(horizontal_conflicts) + "\n")
            log ("total score: " + str(score))
        self.current_score = score
        return score;

    # Reference: https://stackoverflow.com/a/43311126/8214875
    # Finds the diagonal arrays in board
    # Returns conflict count of forward and backward diagonals
    def get_diagonal_conflicts(self, is_test = False, verbose = False):
        if is_test:
            test = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]]
        else:
            test = self.board

        max_col = len(test)
        max_row = len(test[0])
        fdiag = [[] for i in range(max_col + max_row - 1)]
        bdiag = [[] for i in range(len(fdiag))]
        min_bdiag = -max_col + 1

        for y in range(max_col):
            for x in range(max_row):
                fdiag[x+y].append(test[y][x])
                bdiag[-min_bdiag+x-y].append(test[y][x])

        f_diagonal_conflicts = 0

        for diagonal in fdiag:
            num_queens_in_diagonal = len(diagonal) - Counter(diagonal)[0]
            if (num_queens_in_diagonal >= 2):
                f_diagonal_conflicts += combination(num_queens_in_diagonal, 2)

        b_diagonal_conflicts = 0
        for diagonal in bdiag:
            num_queens_in_diagonal = len(diagonal) - Counter(diagonal)[0]
            if (num_queens_in_diagonal >= 2):
                b_diagonal_conflicts += combination(num_queens_in_diagonal, 2)

        if (verbose):
            log("Forward diagonals:")
            log(fdiag)
            log("f_diagonal_conflicts: " + str(f_diagonal_conflicts) + "\n")
            log("Backward diagonals:")
            log(bdiag)
            log("b_diagonal_conflicts: " + str(b_diagonal_conflicts) + "\n")

        return f_diagonal_conflicts, b_diagonal_conflicts

class Queen:
    def __init__(self,i=None,j=None):
        self.row = i
        self.col = j
        # A queen is uniquely identified by its column number (starting from index 1)
        self.id = self.col + 1

    # Represent queen by a red Q
    def __repr__(self):
        return colored('Q','red')

    # Update queen's placement
    def update_row(self, new_row):
        self.row = new_row

    # Print a queen's location in the form of "[i,j]"
    def print_location(self):
        if (self.row != None and self.col != None):
            print ("[" + str(self.row) + ", " + str(self.col) + "]")
        else:
            print('Not placed on board')
