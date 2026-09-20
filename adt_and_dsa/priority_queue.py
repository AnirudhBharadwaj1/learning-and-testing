from typing import Any
from math import floor

class PriorityQueue:
    """
    Implementation for Priority Queue ADT
    Properties:
        - Nearly complete binary tree (every level filled except last which is filled left to right)
        - Max-heap property (each node has value greater than or equal to its children)
    """
    _lst: list

    def __init__(self) -> None:
        self._lst = [None]

    def insert(self, x: Any):
        """
        Inserts element x into the priority queue
        Achieves Theta(logn)
        """
        self._lst.append(x)
        curr = len(self._lst) - 1
        parent = floor(curr / 2)

        # Bubble up
        while self._lst[parent] and self._lst[curr] > self._lst[parent]:
            self._lst[curr], self._lst[parent] = self._lst[parent], self._lst[curr]
            curr = parent
            parent = floor(curr / 2)

    def get_max(self) -> Any | None:
        """
        Retrieves the maximum element from the priority queue
        Achieves Theta(1)
        """
        if len(self._lst) >= 2:
            return self._lst[1]

        return None

    def _get_right_left(self, i: int) -> tuple:
        """Return the indices of the left and right subtrees"""
        return 2 * i, 2 * i + 1

    def extract_max(self) -> Any:
        """
        Pops the maximum element from the priority queue
        Achieves Theta(logn)
        """
        max_val = self._lst[1]
        self._lst[1] = self._lst.pop(-1)

        # Bubble down the value
        curr = 1
        left, right = self._get_right_left(curr)
        length = len(self._lst)

        while left < length or right < length:
            # Bubble down the max
            left_val = self._lst[left] if left < length else -1
            right_val = self._lst[right] if right < length else -1

            # Swap with left
            if left_val > right_val:
                self._lst[curr], self._lst[left] = self._lst[left], self._lst[curr]
                curr = left

            # Swap with right
            else:
                self._lst[curr], self._lst[right] = self._lst[right], self._lst[curr]
                curr = right

            left, right = self._get_right_left(curr)

        return max_val
        
    def increase_priority(self, x: Any, k: Any) -> None:
        """
        Increase the priority of an element x to k in the priority queue
        This operation finds the first matching instance and updates it
        Achieves Theta(logn)
        """
        if x >= k:
            return

        curr = self._lst.index(x)
        self._lst[curr] = k
        parent = floor(curr / 2)

        # Bubble up
        while self._lst[parent] and self._lst[curr] > self._lst[parent]:
            self._lst[curr], self._lst[parent] = self._lst[parent], self._lst[curr]
            curr = parent
            parent = floor(curr / 2)

    def __str__(self) -> str:
        """Easier visualization"""
        final = ""
        level = 0
        i = 1

        while i < len(self._lst):
            tmp = "\t" * level
            for item in self._lst[i:i+2**level]:
                tmp += f"{item}\t\t"
                i += 1

            final += f"{tmp}\n"
            level += 1

        return final

if __name__ == "__main__":
    pq = PriorityQueue()
    pq.insert(15)
    pq.insert(5)
    pq.insert(10)
    pq.insert(3)
    pq.insert(7)
    pq.insert(20)
    print(pq)
    print("-----------------------------------------------------------------------------")

    val = pq.extract_max()
    print(f"Max Value: {val}")
    print(pq)
    print("-----------------------------------------------------------------------------")

    pq.increase_priority(3, 12)
    print(pq)
    print("-----------------------------------------------------------------------------")