from typing import Any
from node import LLNode

class Stack:
    """Implementation of a stack"""
    _stack: list

    def __init__(self) -> None:
        """Initializes the stack instance"""
        self._stack = []

    def push(self, x: Any) -> None:
        """Pushes an item onto the stack"""
        self._stack.append(x)

    def pop(self) -> Any | None:
        """Pops the top element off the stack"""
        if self._stack:
            return self._stack.pop(-1)

    def peek(self) -> Any | None:
        """Returns the top element off the stack"""
        if self._stack:
            return self._stack[-1]

    def __str__(self) -> str:
        """String representation for stack"""
        return str(self._stack)

    def __repr__(self) -> str:
        """String representation for stack"""
        return str(self)

class Queue:
    """Implementation of a Queue using linked list approach for O(1) operations"""
    _head: LLNode
    _tail: LLNode

    def __init__(self) -> None:
        """Initializes an instance of a queue"""
        self._head, self._tail = None, None

    def enqueue(self, x: Any) -> None:
        """Adds an item into the queue"""
        new_node = LLNode(x)

        if not self._head:
            self._head = new_node
            self._tail = new_node

        else:
            self._tail.set_next(new_node)
            self._tail = new_node

    def dequeue(self) -> Any | None:
        """Dequeues the first element from the queue"""
        val = None
        if self._head:
            val = self._head.get_val()
            self._head = self._head.get_next()

            if self._head is None:
                self._tail = None

        return val

    def peek(self) -> Any | None:
        """Returns the first element in the queue"""
        if self._head:
            return self._head.get_val()

        return None

    def __str__(self) -> str:
        """String representation for queue"""
        curr = self._head
        out = "["

        while curr is not None:
            out += str(curr.get_val()) + ", "
            curr = curr.get_next()

        return out[:-2] + "]"

    def __repr__(self) -> str:
        """String representation for queue"""
        return str(self)

if __name__ == "__main__":
    s = Stack()
    s.push(1)
    s.push(2)
    s.push(3)

    print("Stack:", s)
    print("Peek:", s.peek())
    print("Pop:", s.pop())
    print("Pop:", s.pop())
    print("Peek:", s.peek())
    print("Pop:", s.pop())
    print("Stack:", s)
    print("Pop:", s.pop())

    print("\n------------------------------------------------")

    q = Queue()
    q.enqueue(1)
    q.enqueue(2)
    q.enqueue(3)

    print("Queue:", q)
    print("Peek:", q.peek())
    print("Dequeue:", q.dequeue())
    print("Peek:", q.peek())

    q.enqueue(4)

    print("Queue:", q)
    print("Dequeue:", q.dequeue())
    print("Dequeue:", q.dequeue())
    print("Dequeue:", q.dequeue())

    print("Peek:", q.peek())
    print("Dequeue:", q.dequeue())

    q.enqueue(5)
    print("Peek:", q.peek())
    print("Dequeue:", q.dequeue())
    print("Queue:", q)