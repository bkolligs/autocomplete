from cProfile import Profile
from trie import Trie


def profile_trie() -> list:
    trie = Trie()
    keys = ["the", "there", "their", "robot", "robot1", "robot2_b", "robber", "robbed"]

    for k in keys:
        trie.insert(k)

    tests = trie.search("rob")
    return tests


if __name__ == "__main__":
    with Profile() as pr:
        profile_trie()
    
    pr.dump_stats("stats.prof")
