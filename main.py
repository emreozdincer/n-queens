import random
import n_queens as game
import pdb, inspect # Debug

# Options
get_board_size = False # Get board size N as user input

if __name__ == "__main__":
    if get_board_size:
        n = int(raw_input("Enter board size as integer n: "))
    else:
        n = 5

    # Initialize a game board with n elements.
    board = game.Board(n)
    print ("Game board initialized with " + str(n) + " elements.")
    # Initialize n queens, and place them on the board column by column
    queens = [None] * n
    # row_setup = [1,4,0,0,3]
    for column in range(n):
        row = random.randint(0,n-1);
        # row = row_setup[column]
        queens[column] = game.Queen(row, column)
        board.update_element(queens[column], row, column)

    print (str(n) + " queens are randomly placed on board.")
    print (board)

    # game = n_queens.game(n)
    game.hill_climb(board,queens)

    # print(queens)
