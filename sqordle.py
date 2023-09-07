
import pickle
import os
from trie import TrieNodeIterative
import time

MIN_WORD_LEN = 4
DICT_SAVE_NAME = 'dict.pkl'
INV_CHARACTER = '-'


def is_valid(i, j, max):
    return 0 <= i < max and 0 <= j < max


def process_input_file(file_name):
    board = []
    data = []
    with open(file_name, 'r') as fp:
        data = fp.readlines()

    for line in data:
        # Assume spaces and - are empty spaces
        row = []
        for char in line:
            if char == ' ' or char == INV_CHARACTER:
                row.append(INV_CHARACTER)
            elif char != '\n':
                row.append(char.lower())
        board.append(row)
    return board


def build_dictionary(file_name):
    root = TrieNodeIterative('')
    with open(file_name, 'r') as fp:
        line = 'inv'
        while line != '':
            line = fp.readline()
            root.add(line.strip())
    return root


def get_neighbors(board: list[list[str]], string: str, row: int, column: int, visited: set[tuple[int, int]]):
    neighbors = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            x = row + i
            y = column + j
            new_set = visited.copy()
            new_set.add((row, column))
            valid = is_valid(x, y, len(board))
            contained = (x, y) not in new_set
            if valid and contained:
                neighbors.append((string + board[x][y], (x, y), new_set))
    return neighbors


def search_board(dictionary: TrieNodeIterative, board):
    # Try to start at each different value
    result = set()
    needs_evaluation = []
    for i in range(len(board)):
        for j in range(len(board)):
            needs_evaluation.append((board[i][j], (i, j), set()))

    while len(needs_evaluation) > 0:
        current_string, indexes, visited = needs_evaluation.pop(0)

        # See if this is a word
        if dictionary.is_valid_word(current_string) and len(current_string) >= MIN_WORD_LEN:
            result.add(current_string)

        # Add Neighbors if they can possibly have valid words
        for neighbor in get_neighbors(board, current_string, indexes[0], indexes[1], visited):
            if dictionary.is_valid_prefix(neighbor[0]):
                needs_evaluation.append(neighbor)
    return result


if __name__ == '__main__':
    board = process_input_file('input.txt')
    start = time.time()
    root = None
    # Get Dictionary
    if os.path.exists(DICT_SAVE_NAME):
        with open(DICT_SAVE_NAME, 'rb') as fp:
            root = pickle.load(fp)
    else:
        root = build_dictionary('master_dictionary.txt')
    print(f'Dictionary Load Time: {time.time() - start}')
    start = time.time()
    # Perform Search
    result = search_board(root, board)
    print(f'Search Time: {time.time() - start}')
    result = list(result)
    result.sort()

    # Output Resulting Words
    with open('output.txt', 'w') as fp:
        for line in result:
            fp.write(f'{line}\n')

    # Save dictionary for later
    with open(DICT_SAVE_NAME, 'wb') as fp:
        pickle.dump(root, fp)
