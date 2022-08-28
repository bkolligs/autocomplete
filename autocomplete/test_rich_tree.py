from __future__ import annotations
from rich.tree import Tree
from rich import print


class Node:
    def __init__(self, value) -> None:
        self.value = value
        self._children = []

    def add_child(self, child: Node | list):
        if isinstance(child, list):
            self._children.extend(child)
        else:
            self._children.append(child)


def traverse(node: Node):
    sub_tree = Tree(node.value)
    for child in node._children:
        sub_tree.add(traverse(child))

    return sub_tree


if __name__ == "__main__":
    root = Node("root")
    n1 = Node("1")
    n2 = Node("2")
    n3 = Node("3")
    n12 = Node("1.2")
    n13 = Node("1.3")
    n21 = Node("2.1")
    n31 = Node("3.1")
    root.add_child([n1, n2, n3])
    n1.add_child([n12, n13])
    n2.add_child(n21)
    n3.add_child(n31)
    tree = traverse(root)

    print(tree)
