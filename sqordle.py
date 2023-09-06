
import pickle
import os
from trie import TrieNodeIterative
import time

MIN_WORD_LEN = 4
DICT_SAVE_NAME = 'dict.pkl'


def is_valid(i, j, max):
    return 0 <= i < max and 0 <= j < max


def build_dictionary(file_name):
    root = TrieNodeIterative('')
    with open(file_name, 'r') as fp:
        data = fp.readlines()
        for line in data:
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
    board = [
        ['c', 'n', 'v', 't'],
        ['a', 'c', 'o', 'i'],
        ['d', 'p', 'e', 't'],
        ['e', 't', 'u', 'm'],
    ]

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
