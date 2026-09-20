from typing import Any

class HashTable:
    """
    Implementation of Hash Table using chaining to avoid collisions
    Hashing Function: index = hash(key) % self._capacity
    """
    _table: list
    _capacity: int

    def __init__(self, capacity: int = 10):
        """Initializer for the class"""
        self._table = [[]] * capacity
        self._capacity = capacity

    def _get_idx(self, key: Any) -> None:
        """Returns the index of that the key should have"""
        return hash(key) % self._capacity

    def insert(self, key: Any, val: Any) -> None:
        """Inserts the key value pair into the hash table and handles collisions"""
        idx = self._get_idx(key)

        if not self._table[idx]:
            self._table[idx] = [[key, val]]

        else:
            # Check if the key already exists
            for item in self._table[idx]:
                if item[0] == key:
                    item[1] = val

            self._table[idx].append([key, val])

    def get(self, key: Any) -> Any | None:
        """Gets the value for a key"""
        idx = self._get_idx(key)

        if self._table[idx]:
            for item in self._table[idx]:
                if item[0] == key:
                    return item[1]

    def contains(self, key: Any) -> bool:
        """Returns whether the key exists in the table"""
        idx = self._get_idx(key)

        if self._table[idx]:
            for item in self._table[idx]:
                if item[0] == key:
                    return True

        return False

    def delete(self, key: Any) -> None:
        """Delete the key from the hash table"""
        idx = self._get_idx(key)
        del_item = None

        if self._table[idx]:
            for item in self._table[idx]:
                if item[0] == key:
                    del_item = item

            if del_item:
                self._table[idx].remove(del_item)

    def __str__(self) -> str:
        """String representation for the class"""
        out = "[\n"

        for i in self._table:
            out += str(i) + "\n"

        return out + "]"

    def __repr__(self) -> str:
        """String representation for the class"""
        return str(self)

if __name__ == "__main__":
    ht = HashTable()
    ht.insert(1, 'a')
    ht.insert(2, 'b')
    ht.insert(3, 'c')
    ht.insert(4, 'd')
    ht.insert(5, 'e')

    print(ht)
    print("")

    ht.insert(11, 'aa')
    ht.insert(21, 'aaa')

    print(ht)
    print("")

    print("3: ", ht.get(3))
    print("5: ", ht.get(5))
    print("10: ", ht.get(10))

    print(ht.contains(2))
    print(ht.contains(10))

    ht.delete(3)
    ht.delete(2)
    ht.delete(100)
    print(ht)