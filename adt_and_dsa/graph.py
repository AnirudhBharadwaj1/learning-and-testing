from typing import Any
from node import GraphNode

class Graph:
    """Implementation of Disjoint Set ADT"""
    _nodes: dict[Any, GraphNode]
    _is_directed: bool

    def __init__(self, directed=False) -> None:
        """Initialize this instance of a graph"""
        self._nodes = {}
        self._is_directed = directed

    def add_vertex(self, x: Any) -> None:
        """Add a vertex to the graph"""
        if x not in self._nodes:
            self._nodes[x] = GraphNode(x)

    def remove_vertex(self, x: Any) -> None:
        """Remove a vertex and all edges connected to it"""
        if x not in self._nodes:
            return

        node = self._nodes[x]

        # Remove this node from all of its neighbors
        for neighbor in self._nodes.values():
            neighbor.remove_neighbor(node)

        del self._nodes[x]

    def add_edge(self, u: Any, v: Any) -> None:
        """Add an edge from node u to node v"""
        self.add_vertex(u)
        self.add_vertex(v)

        self._nodes[u].add_neighbor(self._nodes[v])

        if not self._is_directed:
            self._nodes[v].add_neighbor(self._nodes[u])

    def has_vertex(self, x: Any) -> bool:
        """Return whether x is a vertex in the graph"""
        return x in self._nodes

    def has_edge(self, u: Any, v: Any) -> bool:
        """Return whether an edge from u to v exists"""
        if u not in self._nodes or v not in self._nodes:
            return False

        return self._nodes[u].has_neighbor(self._nodes[v])

    def neighbors(self, x: Any) -> set[Any]:
        """Return values fo all neighbors of x"""
        if x not in self._nodes:
            return set()

        return {node.get_val() for node in self._nodes[x].get_neighbors()}

    def __contains__(self, x: Any) -> bool:
        """Return if x is present in the graph"""
        return x in self._nodes

    def __len__(self) -> int:
        """Return the number of vertices"""
        return len(self._nodes)

    def __str__(self) -> str:
        """Return string representation of the graph"""
        lines = []

        for value, node in self._nodes.items():
            neighbors = ", ".join(
                str(neighbor.get_val())
                for neighbor in node.get_neighbors()
            )
            lines.append(f"{value}: [{neighbors}]")

        return "\n".join(lines)