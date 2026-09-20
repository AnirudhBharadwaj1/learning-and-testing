from __future__ import annotations
from typing import Any

class Node:
    """Superclass for general type node"""
    _val: Any

    def __init__(self, val: Any) -> None:
        """Initialize instance of Node"""
        self._val = val

    def get_val(self) -> Any:
        """Return this node's value"""
        return self._val

    def set_val(self, val: Any) -> None:
        """Sets the value of this node"""
        self._val = val

class LLNode(Node):
    """A class for linked list nodes"""
    _next: LLNode

    def __init__(self, val: Any) -> None:
        """Initialize instance of LLNode"""
        super().__init__(val)
        self._next = None

    def get_next(self) -> LLNode | None:
        """Return the next node in the sequence"""
        return self._next

    def set_next(self, next: LLNode) -> None:
        """Set the next node in the sequence"""
        self._next = next

class DoublyLLNode(LLNode):
    """A class for doubly linked list nodes"""
    _prev: DoublyLLNode

    def __init__(self, val: Any) -> None:
        """Initialize instance of DoublyLLNode"""
        super().__init__(val)
        self._prev = None

    def get_prev(self) -> DoublyLLNode | None:
        """Return the previous node in the sequence"""
        return self._prev

    def set_prev(self, prev: DoublyLLNode) -> None:
        """Set the previous node in the sequence"""
        self._prev = prev

class BinaryTreeNode(Node):
    """A class for binary tree nodes"""
    _left: BinaryTreeNode
    _right: BinaryTreeNode

    def __init__(self, val: Any) -> None:
        """Initialize instance of BinaryTreeNode"""
        super().__init__(val)
        self._left = None
        self._right = None

    def is_leaf(self) -> bool:
        """Return if this node is a leaf or not"""
        return not self._left and not self._right

    def get_left(self) -> BinaryTreeNode | None:
        """Get the left subtree for this node"""
        return self._left

    def get_right(self) -> BinaryTreeNode | None:
        """Get the right subtree for this node"""
        return self._right

    def set_left(self, left: BinaryTreeNode) -> None:
        """Set the left node for this tree"""
        self._left = left

    def set_right(self, right: BinaryTreeNode) -> None:
        """Set the right node for this tree"""
        self._right = right

class AVLNode(BinaryTreeNode):
    """A class for an AVL Tree node"""
    _height: int

    def __init__(self, val: Any) -> None:
        """Initialize instance of AVLNode"""
        super().__init__(val)
        self._height = 1

    def get_height(self) -> int:
        """Return the height of the node"""
        return self._height

    def set_height(self, height: int) -> None:
        """Set the height of this node"""
        self._height = height

class GraphNode(Node):
    """A class for graph nodes"""
    _neighbors: set[GraphNode]

    def __init__(self, val: Any) -> None:
        """Initialize instance of GraphNode"""
        super().__init__(val)
        self._neighbors = set()

    def get_neighbors(self) -> set[GraphNode]:
        """Return the list of nodes that neighbor this one"""
        return self._neighbors

    def add_neighbor(self, node: GraphNode) -> None:
        """Add neighbor to this node"""
        self._neighbors.add(node)

    def remove_neighbor(self, node: GraphNode) -> None:
        """Remove a neighbor from the set"""
        self._neighbors.discard(node)

    def has_neighbor(self, node: GraphNode) -> bool:
        """Return whether these two nodes are neighbors"""
        return node in self._neighbors