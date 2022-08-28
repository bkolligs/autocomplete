from autocomplete.trie import Trie
from rich import print


def test_trie():
    trie = Trie()
    keys = ["the", "there", "their", "robot", "robot1", "robot2_b", "robber", "robbed"]

    for k in keys:
        trie.insert(k)

    tests = trie.search("rob")
    assert len(tests) == 5

    print("Trie looks like:\n", trie)
