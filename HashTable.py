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

    def search(self, key):
        bucket = key - 1
        bucket_list = self.table[bucket]
        for item in bucket_list:
            if hash(item) == key:
                return item

    def remove(self, key):
        bucket = key - 1
        bucket_list = self.table[bucket]
        for item in bucket_list:
            if hash(item) == key:
                bucket_list.remove(key)
                self.table.remove(bucket)
                self.size = len(self.table)
