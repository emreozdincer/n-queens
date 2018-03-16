from termcolor import colored
from collections import Counter
from math import factorial
import copy
import pdb # Debug

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

# Moves queen to new_row in board
def update_game(new_row, queen, board, verbose = False):
    update_text = colored("\nQueen " + str(queen.id) + " to row " + str(new_row) + "!", 'green')
    old_row = queen.row
    board.update_element(0, old_row, queen.col)
    board.update_element(queen, new_row, queen.col)
    queen.update_row(new_row)

    if (verbose):
        print(update_text)
        print(board)

# Hill Climbing algorithm
def hill_climb(board, queens):
    best_state_found = False
    iteration_count = 0
    while (best_state_found == False and board.current_score != 0):
        iteration_count += 1
        print(colored("\nIteration " + str(iteration_count),'yellow'))
        best_state_found = go_to_next_best_state(board, queens, verbose = True)

    print ('Hit local minimum with score: ' + str(board.current_score))

    if (board.current_score == 0):
        print (colored('Success!', 'green'))
    else:
        print (colored('Fail!','red'))

# Goes to next best state, returns best_state_found
def go_to_next_best_state(board, queens_original, verbose = False):
    n = board.size_n

    print("Initial score: " + str(board.current_score))
    queens = copy.deepcopy(queens_original)
    best_state = copy.deepcopy(board)
    best_score = board.current_score
    best_state_found = True # assume true, set to false if appropriate

    # Calculate scores for every available next state
    # For each queen
    for q_index, queen in enumerate(queens):
        # There exists n-1 rows to explore
        rows_to_explore = [x for x in range(n)]
        rows_to_explore.pop(queen.row)
        # For each unexplored row, check if it yields a better result than current state
        for row in rows_to_explore:
            queens_original_row = queen.row
            next_state = copy.deepcopy(board)
            update_game(row,queen,next_state)
            # Save the next best state & queens if next_state is best yet
            if (next_state.current_score < best_score):
                best_state_found = False
                best_state = next_state
                best_score = next_state.current_score
                moved_queen_index = q_index
                moved_queen_new_row = row
            # Put the explorer queen back to original place
            else:
                queen.update_row(queens_original_row)

    # Update the queens array if they changed
    if not best_state_found:
        queens_original[moved_queen_index].update_row(moved_queen_new_row)

    print best_state
    board.update_state(best_state)
    print("Best iteration score: " + str(board.current_score))
    return best_state_found

class Board:
    # Initializes empty n x n board
    def __init__(self, n):
        self.board = [[0]*n for x in range(n)]
        self.size_n = n

    # Represent the class object as its board
    def __repr__(self):
        # return ('B')
        return ('\n'.join(map(repr, self.board)))

    def print_board(self):
        for row in self.board:
            print row

    def update_element(self, element, row, col):
        self.board[row][col] = element
        self.calculate_score()

    # Updates current board with a new board
    def update_state(self, next_state):
        self.board = next_state.board
        self.current_score = self.calculate_score()

    def get_current_score(self):
        return self.current_score

    # def hill_climb(self, queens):
    #     best_state_found = False
    #     iteration_count = 0
    #     while (True):
    #         print(colored("\nIteration " + str(iteration_count),'green'))
    #         best_state_found = self.go_to_next_best_state(queens, verbose = True)
    #
    #         if (best_state_found):
    #             print ('Hit local minimum with score: ' + str(self.current_score))
    #             break
    #
    #         iteration_count += 1
    #         queens = get_queens_from_board(self, queens)

    # Goes to next best state, while also updating the queens' array
    # def go_to_next_best_state(self, queens_original, verbose = False):
    #     n = self.size_n
    #
    #     print("Initial score: " + str(self.current_score))
    #     best_state = copy.deepcopy(self)
    #     best_score = self.current_score
    #     best_state_found = True # assume true
    #
    #     queens = copy.deepcopy(queens_original)
    #
    #     # Calculate scores for every available next state
    #     # For each queen
    #     for q_index, queen in enumerate(queens):
    #         # There exists n-1 row explorations
    #         rows_to_explore = [x for x in range(n)]
    #         rows_to_explore.pop(queen.row)
    #         # For each row, go to an unexplored row, save its score
    #         for row in rows_to_explore:
    #             next_state = copy.deepcopy(self)
    #             update_game(row,queen,next_state)
    #             # Save the next best state & queens if better
    #             if (next_state.current_score < best_score):
    #                 best_state_found = False
    #                 best_state = next_state
    #                 best_score = next_state.current_score
    #
    #     if DEBUG:
    #         # print best_score
    #         for q in best_queens:
    #             q.print_location()
    #
    #     print best_state
    #     self.update_state(best_state)
    #     print("Best iteration score: " + str(self.current_score))
    #     return best_state_found

    # Calculates each score for current board state
    def calculate_score(self, check_vertical_conflicts = False):
        n = self.size_n
        score = 0
        # Check horizontal conflicts
        # For each row, count the number of queens, save in 'queens_by_rows' array
        queens_by_rows = [0] * n
        vertical_conflicts = 0
        for row in range(n):
            for column in range(n):
                if (isinstance(self.board[row][column], Queen)):
                    queens_by_rows[row] += 1
            if (queens_by_rows[row] >= 2):
                vertical_conflicts += combination(queens_by_rows[row],2)
        log ("queens_by_rows:")
        log (queens_by_rows)
        log("vertical_conflicts: " + str(vertical_conflicts) + "\n")

        # Check vertical conflicts
        # For each column, count the number of queens, save in 'queens_by_columns' array
        if not check_vertical_conflicts:
            pass
        else:
            queens_by_columns = [0] * n
            for column in range(n):
                for row in range(n):
                    if (isinstance(self.board[row][column], Queen)):
                        queens_by_columns[column] += 1
            log ("queens_by_columns:")
            log (queens_by_columns)

        # Check diagonal conflicts
        f_diagonal_conflicts, b_diagonal_conflicts = self.get_diagonal_conflicts()
        score = vertical_conflicts + f_diagonal_conflicts + b_diagonal_conflicts
        log("score: " + str(score))
        self.current_score = score
        return score;

    # Reference: https://stackoverflow.com/a/43311126/8214875
    # Finds the diagonal arrays in board
    # Returns conflict count of forward and backward diagonals
    def get_diagonal_conflicts(self, is_test = False):
        if is_test:
            test = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]]
        else:
            test = self.board

        max_col = len(test)
        max_row = len(test[0])
        # cols = [[] for i in range(max_col)]
        # rows = [[] for i in range(max_row)]
        fdiag = [[] for i in range(max_col + max_row - 1)]
        bdiag = [[] for i in range(len(fdiag))]
        min_bdiag = -max_col + 1

        for y in range(max_col):
            for x in range(max_row):
                # cols[y].append(test[y][x])
                # rows[x].append(test[y][x])
                fdiag[x+y].append(test[y][x])
                bdiag[-min_bdiag+x-y].append(test[y][x])

        f_diagonal_conflicts = 0
        log("Forward diagonals:")
        log(fdiag)
        for diagonal in fdiag:
            num_queens_in_diagonal = len(diagonal) - Counter(diagonal)[0]
            if (num_queens_in_diagonal >= 2):
                f_diagonal_conflicts += combination(num_queens_in_diagonal, 2)
        log("f_diagonal_conflicts: " + str(f_diagonal_conflicts) + "\n")

        b_diagonal_conflicts = 0
        log("Backward diagonals:")
        log(bdiag)
        for diagonal in bdiag:
            num_queens_in_diagonal = len(diagonal) - Counter(diagonal)[0]
            if (num_queens_in_diagonal >= 2):
                b_diagonal_conflicts += combination(num_queens_in_diagonal, 2)
        log("b_diagonal_conflicts: " + str(b_diagonal_conflicts) + "\n")

        return f_diagonal_conflicts, b_diagonal_conflicts

class Queen:
    def __init__(self,i=None,j=None):
        self.row = i
        self.col = j
        # A queen is uniquely identified by its column number (starting from index 1)
        self.id = self.col + 1

    # Represent queens by a red Q
    def __repr__(self):
        return colored('Q','red')

    # Updates queen's placement
    def update_row(self, new_row):
        self.row = new_row

    # Print a queen's location in the form of "[i,j]"
    def print_location(self):
        if (self.row != None and self.col != None):
            print ("[" + str(self.row) + ", " + str(self.col) + "]")
        else:
            print('Not placed on board')
