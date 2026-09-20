from __future__ import annotations
from typing import Any
from node import LLNode, DoublyLLNode

class LinkedList:
    """Implementation of a Linked List"""
    _head: LLNode
    _size: int

    def __init__(self) -> None:
        """Initializer for the instance"""
        self._head = None
        self._size = 0

    def append(self, x: Any) -> None:
        """Append an item to the end of the list"""
        if not self._head:
            self._head = LLNode(x)

        else:
            curr = self._head
            while curr.get_next() is not None:
                curr = curr.get_next()

            curr.set_next(LLNode(x))

        self._size += 1

    def insert(self, x: Any, i: int) -> None:
        """Insert an item into any part of the list"""
        if i < 0:
            raise IndexError("Index cannot be negative")

        if i >= self._size:
            self.append(x)
            return

        new_node = LLNode(x)

        # Insert at the beginning
        if i == 0:
            new_node.set_next(self._head)
            self._head = new_node
            self._size += 1
            return

        curr = self._head

        # Stop on the node before the insert
        for _ in range(i - 1):
            curr = curr.get_next()

        new_node.set_next(curr.get_next())
        curr.set_next(new_node)
        self._size += 1

    def find(self, x: Any) -> int:
        """Return the first index of x and -1 if x is not found"""
        curr = self._head
        i = 0

        while curr is not None:
            if curr.get_val() == x:
                return i

            curr = curr.get_next()
            i += 1

        return -1

    def remove(self, x: Any) -> None:
        """Remove the first occurrence of x"""
        if self._head is None:
            return

        # Remove head
        if self._head.get_val() == x:
            self._head = self._head.get_next()
            self._size -= 1
            return

        curr = self._head

        while curr.get_next() is not None:
            if curr.get_next().get_val() == x:
                curr.set_next(curr.get_next().get_next())
                self._size -= 1
                return

            curr = curr.get_next()

    def pop(self, x: Any, i: int) -> None:
        """Pop an element from the list and return it"""
        if self._size == 0:
            raise IndexError("Cannot pop from empty list")

        if i < 0:
            i += self._size

        if i < 0 or i >= self._size:
            raise IndexError("Index out of range")

        # Remove the head
        if i == 0:
            value = self._head.get_val()
            self._head = self._head.get_next()
            self._size -= 1
            return value

        curr = self._head

        # Stop on the node before the insert
        for _ in range(i - 1):
            curr = curr.get_next()

        node = curr.get_next()
        value = node.get_val()

        curr.set_next(node.get_next())

        self._size -= 1
        return value

    def get(self, i: int) -> Any | None:
        """Return the item at index i"""
        if i < 0 or i >= self._size:
            return None

        curr = self._head

        for _ in range(i):
            curr = curr.get_next()

        return curr.get_val()

    def size(self) -> int:
        """Return the size of the linked list"""
        return self._size

    def clear(self) -> None:
        """Remvoes all elements"""
        self._head = None
        self._size = 0

    def __str__(self) -> str:
        """String representation for the linked list"""
        out = ""
        curr = self._head

        while curr is not None:
            out += str(curr.get_val())
            out += " -> "
            curr = curr.get_next()

        return out[:-4]

    def __repr__(self) -> str:
        """String representation for the linked list"""
        return str(self)

class DoublyLinkedList:
    """Implementation of a doubly linked list"""
    _head: DoublyLLNode
    _tail: DoublyLLNode
    _size: int

    def __init__(self) -> None:
        """Initializer for the instance"""
        self._head = None
        self._tail = None
        self._size = 0

    def append(self, x: Any) -> None:
        """Append an item to the end of the list"""
        new_node = DoublyLLNode(x)

        if not self._head:
            self._head = new_node
            self._tail = new_node

        else:
            self._tail.set_next(new_node)
            new_node.set_prev(self._tail)
            self._tail = new_node

        self._size += 1

    def _get_node(self, i: int) -> DoublyLLNode:
        """Return the node at index i"""
        # Optimize for doubly ll
        if i < self._size // 2:
            curr = self._head

            for _ in range(i):
                curr = curr.get_next()

        else:
            curr = self._tail

            for _ in range(self._size - 1, i, -1):
                curr = curr.get_prev()

        return curr

    def insert(self, x: Any, i: int) -> None:
        """Insert an item into any part of the list"""
        if i < 0:
            raise IndexError("Index cannot be negative")

        if i >= self._size:
            self.append(x)
            return

        new_node = DoublyLLNode(x)

        # Insert at head
        if i == 0:
            new_node.set_next(self._head)
            self._head.set_prev(new_node)
            self._head = new_node
            self._size += 1
            return

        curr = self._get_node(i)
        prev_node = curr.get_prev()

        new_node.set_prev(prev_node)
        new_node.set_next(curr)

        prev_node.set_next(new_node)
        curr.set_prev(new_node)
        
        self._size += 1

    def find(self, x: Any) -> int:
        """Return the first index of x and -1 if x is not found"""
        curr = self._head
        i = 0

        while curr is not None:
            if curr.get_val() == x:
                return i

            curr = curr.get_next()
            i += 1

        return -1

    def _remove_node(self, node: DoublyLLNode) -> None:
        """Remove a specific node from the list"""
        prev_node = node.get_prev()
        next_node = node.get_next()

        if prev_node is None:
            self._head = next_node
        else:
            prev_node.set_next(next_node)

        if next_node is None:
            self._tail = prev_node
        else:
            next_node.set_prev(prev_node)

        self._size -= 1

    def remove(self, x: Any) -> None:
        """Remove the first occurrence of x"""
        curr = self._head

        while curr is not None:
            if curr.get_val() == x:
                self._remove_node(curr)
                return

    def pop(self, x: Any, i: int) -> None:
        """Pop an element from the list and return it"""
        if self._size == 0:
            raise IndexError("Cannot pop from empty list")

        if i < 0:
            i += self._size

        if i < 0 or i >= self._size:
            raise IndexError("Index out of range")

        node = self._get_node(i)
        value = node.get_val()

        self._remove_node(node)

        return value
        
    def get(self, i: int) -> Any | None:
        """Return the item at index i"""
        if i < 0 or i >= self._size:
            return None

        return self._get_node(i).get_val()

    def size(self) -> int:
        """Return the size of the linked list"""
        return self._size

    def clear(self) -> None:
        """Remvoes all elements"""
        self._head = None
        self._tail = None
        self._size = 0

    def __str__(self) -> str:
        """String representation for the linked list"""
        out = ""
        curr = self._head

        while curr is not None:
            out += str(curr.get_val())
            out += " <-> "
            curr = curr.get_next()

        return out[:-5]

    def __repr__(self) -> str:
        """String representation for the linked list"""
        return str(self)