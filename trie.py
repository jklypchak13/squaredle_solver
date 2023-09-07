from typing import Dict


class TrieNodeIterative:
    def __init__(self, letter: str):
        self.letter: str = letter
        self.children: Dict[str, TrieNodeRecursive] = {}
        self.length: int = 0
        self.is_word: bool = False

    def add(self, word: str):
        """add the given word to the trie

        Args:
            word (str): the word to add to the dictionary
        """
        node = self
        for letter in word:
            node.length += 1
            node = node.children.setdefault(letter, TrieNodeIterative(letter))
        node.is_word = True
        node.length += 1

    def is_valid_prefix(self, prefix: str) -> bool:
        """check if the given prefix has further words

        Args:
            word (str): the prefix to check

        Returns:
            bool: true if words exist with the given prefix
        """
        node = self
        for letter in prefix:
            try:
                node = node.children[letter]
            except KeyError:
                return False
        return node.length != 1

    def is_valid_word(self, word: str) -> bool:
        """check if the given word has been added to the trie

        Args:
            word (str): the word to test

        Returns:
            bool: true if the word was previously added to the trie
        """
        node = self
        for letter in word:
            try:
                node = node.children[letter]
            except KeyError:
                return False
        return node.is_word


class TrieNodeRecursive:
    """a trie data structure, representing a dictionary of all words at the root, and each
       individual node containing all words that have that prefix
    """

    def __init__(self, letter: str):
        self.letter: str = letter
        self.children: Dict[str, TrieNodeRecursive] = {}
        self.length: int = 0
        self.is_word: bool = False

    def add(self, word: str):
        """add the given word (or remainder of word) to this trie

        Args:
            word (str): the word to add to the trie
        """
        self.length += 1
        if len(word) == 0:
            self.is_word = True
        else:
            letter = word[0]
            if letter not in self.children.keys():
                self.children[letter] = TrieNodeRecursive(letter)
            self.children[letter].add(word[1:])

    def is_valid_prefix(self, word: str) -> bool:
        """determines if a valid word contains the given prefix

        Args:
            word (str): the prefix to check

        Returns:
            bool: True if a word with that prefix is valid in the trie
        """
        if len(word) == 0:
            return self.length != 0
        elif word[0] not in self.children.keys():
            return False
        return self.children[word[0]].is_valid_prefix(word[1:])

    def is_valid_word(self, word: str) -> bool:
        """determine if the given word is valid according to the trie

        Args:
            word (str): the word (or remainder of word) to test

        Returns:
            bool: True if the word is valid
        """
        if len(word) == 0:
            return self.is_word
        elif word[0] not in self.children.keys():
            return False
        return self.children[word[0]].is_valid_word(word[1:])
