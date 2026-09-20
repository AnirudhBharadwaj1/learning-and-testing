from typing import Any

class DisjointSet:
    """
    Implementation of Disjoint Set ADT
    
    Attributes:
        - _parent: Maps elements to their set representatives
        - _rank: Maps elements to the number of elements mapped to them

    Properties:
        - Uses path compression and union by rank to achieve amortized cost of O(\alpha(n))
    """
    _parent: dict
    _rank: dict

    def __init__(self) -> None:
        """Initializes the instance of the disjoint set"""
        self._parent = {}
        self._rank = {}

    def make_set(self, x: Any) -> None:
        """Create a new set for the element x"""
        self._parent[x] = x
        self._rank[x] = 0

    def find_set(self, x: Any) -> Any:
        """
        Finds the represenative of the set for an element x
        Uses path compression to make future searches faster
        """
        if self._parent[x] != x:
            self._parent[x] = self.find_set(self._parent[x])

        return self._parent[x]

    def link(self, x: Any, y: Any) -> None:
        """
        Join two set representatives into one set
        Uses union by rank to determine the order of linking
        """
        # Don't modify rank since the height would be the other representative has higher rank anyways
        if self._rank[x] > self._rank[y]:
            self._parent[y] = x

        elif self._rank[y] > self._rank[x]:
            self._parent[x] = y

        # Modify rank since they had the same rank as each other
        else:
            self._parent[y] = x
            self._rank[x] += 1

    def union(self, x: Any, y: Any) -> None:
        """Combine the two sets containing x and y"""
        repr_x = self.find_set(x)
        repr_y = self.find_set(y)

        if repr_x != repr_y:
            self.link(repr_x, repr_y)