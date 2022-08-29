from __future__ import annotations
from rich.tree import Tree


class TrieNode:
    def __init__(self, value: str):
        """A node in the Trie data structure.

        Parameters
        ----------
        value : str
            The character this node stores.
        """
        # the character stored in this node
        self.value = value

        # whether this can be the end of a word
        self.is_end = False

        # a counter indicating how many times a word is inserted
        # (if this node's is_end is True)
        self.counter = 0
        self.children: dict[str, TrieNode] = {}

    def __rich__(self) -> str:
        """Return a representation of this Trie node for rich printing."""
        return f"[bold green]{self.value}"


class Trie:
    """A trie data structure.

    The root node does not store any values.
    """

    def __init__(self, keys: list[str] | None = None):
        self.root = TrieNode("")
        if keys is not None:
            for k in keys:
                self.insert(k)

    def __rich__(self) -> str:
        """Return a representation of this Trie for rich printing."""
        tree = self._traverse_full(self.root)
        tree.label = "[bold]Trie\n"
        return tree

    def insert(self, word):
        """Insert a word into the Trie.

        Parameters
        ----------
        word : str
            The word to insert.
        """
        node = self.root

        for char in word:
            # if a character is not in the node's children, create it
            if char in node.children:
                node = node.children[char]
            else:
                new_node = TrieNode(char)
                node.children[char] = new_node
                node = new_node

        # Mark the end of a word
        node.is_end = True

        # Increment the counter to indicate that we are adding this word again.
        node.counter += 1

    def _traverse_full(self, node: TrieNode):
        """Fully traverse the tree for viewing purposes.

        Parameters
        ----------
        node : TrieNode
            The starting node to traverse from.

        Returns
        -------
        Tree
            Rich tree to view.
        """
        tree = Tree(
            node.value,
            style="red" if node.is_end else "green",
            guide_style="bold bright_blue",
        )
        for child in node.children.values():
            tree.add(self._traverse_full(child))

        return tree

    def _traverse_remaining_words(self, node: TrieNode, prefix: str):
        """Traverse the Trie using depth first search.

        Parameters
        ----------
        node : TrieNode
            The node to start with.
        prefix : str
            The query prefix to search the trie.
        """
        output = []
        if node.is_end:
            output.append((prefix + node.value, node.counter))

        for child in node.children.values():
            output.extend(self._traverse_remaining_words(child, prefix + node.value))

        return output

    def search(self, prefix: str):
        """Search for a prefix in the Trie and return all words that contain the prefix.

        Parameters
        ----------
        prefix : str
            The query prefix.

        Returns
        -------
        list
            All words that contain the prefix.
        """
        node = self.root

        # Check if the prefix is in the trie
        for char in prefix:
            if char in node.children:
                node = node.children[char]
            else:
                # cannot found the prefix, return empty list
                return []

        # Traverse the trie to get all candidates
        output = self._traverse_remaining_words(node, prefix[:-1])

        # Sort the results in reverse order and return
        return sorted(output, key=lambda x: x[1], reverse=True)

    def query(self, prefix: str) -> list:
        """Display the trie search results in a format that's easy to read.

        Parameters
        ----------
        prefix : str
            The query prefix.

        Returns
        -------
        list
            The words that contain this prefix.
        """
        raw = self.search(prefix)
        output = "\t".join([result[0] for result in raw])
        return output
