## Synopsis

Python implementation of some local search algorithms for N-Queens problem:
* Hill Climbing
* First-Choice Hill Climbing
* Simulated Annealing

## Usage

Set options in `main.py`:

```
board_size = 10
num_restarts = 10
# ...
```

Initialize with
` game = n_queens.game(n) `

Run algorithms with
`game.hill_climb()`
or
`game.first_best_hill_climb()`

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
