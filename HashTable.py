class HashTable:

    def __init__(self, size=40):
        self.table = []
        self.size: size = size
        for index in range(size):
            self.table.append([])

    def insert(self, item):
        bucket = hash(item) - 1
        bucket_list = self.table[bucket]
        bucket_list.append(item)

    def search(self, key: int):
        bucket = key - 1
        bucket_list = self.table[bucket]
        for item in bucket_list:
            if hash(item) == key:
                return item

    def remove(self, key: int):
        bucket = key - 1
        bucket_list = self.table[bucket]
        for item in bucket_list:
            if hash(item) == key:
                bucket_list.remove(item)

    def is_empty(self) -> bool:
        return not any(self.table)

    def is_full(self) -> bool:
        return all(self.table)
