class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [[None, None]] * self.size
        self.added_count = 0

    def _hash(self, key):
        return hash(key) % self.size

    def _linear_find(self, index):
        start_index = index
        while self.table[index][0] is not None:
            index = self._new_index(index)
            if index == start_index:
                raise Exception("HashTable is full")
        return index

    def insert(self, key, value):
        if self.added_count == self.size:
            raise Exception("HashTable is full")

        index = self._hash(key)

        if self.table[index][0] is None:
            self.table[index] = [key, value]
        else:
            index = self._linear_find(index)
            self.table[index] = [key, value]

        self.added_count += 1

    def update(self, key, value):
        index = self._hash(key)
        start_index = index

        while self.table[index][0] is not None:

            if self.table[index][0] == key:
                self.table[index] = [key, value]
                return True
            index = self._new_index(index)

            if index == start_index:
                break

        return False

    def search(self, key):
        index = self._hash(key)
        start_index = index

        while self.table[index][0] is not None:
            if self.table[index][0] == key:
                return self.table[index][1]

            index = self._new_index(index)

            if index == start_index:
                break

        return None

    def delete(self, key):
        index = self._hash(key)
        start_index = index

        while self.table[index][0] is not None:

            if self.table[index][0] == key:
                self.table[index] = [None, None]
                self.added_count -= 1
                return True

            index = self._new_index(index)

            if index == start_index:
                break

        return False

    def _new_index(self, cur_index):
        cur_index += 1
        cur_index %= self.size
        return cur_index

    def __str__(self):
        result = '\n'.join(str(x) for x in self.table)
        result = "HashTable:\n" + result
        return result
