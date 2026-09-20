from typing import Any
from node import AVLNode

class AVLTree:
    """Implementation of the AVL Tree ADT"""
    _root: AVLNode | None

    def __init__(self) -> None:
        self._root = None

    def _get_node_height(self, node: AVLNode | None) -> int:
        """Ensure the node exists before returning its height"""
        if not node:
            return 0
        return node.get_height()

    def _update_height(self, node: AVLNode) -> None:
        """Update the height of the given node"""
        node.set_height(1 + max(self._get_node_height(node.get_left()), self._get_node_height(node.get_right())))

    def _get_balance(self, node: AVLNode | None) -> int:
        """Get the balance factor of a node"""
        if not node:
            return 0

        return self._get_node_height(node.get_left()) - self._get_node_height(node.get_right())

    def _rotate_right(self, node: AVLNode) -> AVLNode:
        """Performs a right rotation around node"""
        left = node.get_left()
        left_right = left.get_right()

        left.set_right(node)
        node.set_left(left_right)

        self._update_height(node)
        self._update_height(left)

        return left

    def _rotate_left(self, node: AVLNode) -> AVLNode:
        """Performs a left rotation around node"""
        right = node.get_right()
        right_left = right.get_left()

        right.set_left(node)
        node.set_right(right_left)

        self._update_height(node)
        self._update_height(right)

        return right

    def _rebalance(self, node: AVLNode) -> AVLNode:
        """Maintain the AVL property from the node downwards"""
        self._update_height(node)
        balance = self._get_balance(node)

        # If tree is left heavy
        if balance > 1:
            # Left right case
            if self._get_balance(node.get_left()) < 0:
                node.set_left(self._rotate_left(node.get_left()))

            # Left left case
            return self._rotate_right(node)

        # If tree is right heavy
        if balance < -1:
            # Right left case
            if self._get_balance(node.get_right()) > 0:
                node.set_right(self._rotate_right(node.get_right()))

            # Right right case
            return self._rotate_left(node)

        return node

    def _insert_helper(self, node: AVLNode | None, x: Any) -> AVLNode:
        """Helper function for inserting into the AVL tree"""
        if node is None:
            return AVLNode(x)

        if x < node.get_val():
            node.set_left(self._insert_helper(node.get_left(), x))

        elif x > node.get_val():
            node.set_right(self._insert_helper(node.get_right(), x))

        else:
            return node

        return self._rebalance(node)

    def insert(self, x: Any) -> None:
        """
        Insert a value into the AVL Tree
        Achieves Theta(logn)
        """
        self._root = self._insert_helper(self._root, x)

    def search(self, x: Any) -> AVLNode | None:
        """
        Run a standard binary tree search to retrieve the node with the desired value
        Achieves Theta(logn)
        """
        curr = self._root

        while curr is not None:
            if x == curr.get_val():
                return curr

            elif x < curr.get_val():
                curr = curr.get_left()

            else:
                curr = curr.get_right()

        return None

if __name__ == "__main__":
    avl = AVLTree()