## Synopsis

Python implementation of Hill Climbing algorithm for N-Queens problem

## Usage
Choose options in `main.py`:

```
ask_board_size = False
use_colors = False
num_restarts = 10
```
Use the algorithm with:
```
game = n_queens.game(n)
game.hill_climb()
```
Further play with options in `n_queens` files by changing `verbose` arguments and the `DEBUG` variable.

## Motivation

Done for CS404 - Artificial Intelligence course in Sabanci University in March 2018.

## Prerequisites

There are no prerequisites.

Optionally, install Termcolor for better visuals
`pip install termcolor`

Set the relevant option
`use_colors = True`

## License

[MIT](./LICENSE)
