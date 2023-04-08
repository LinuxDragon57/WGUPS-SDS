

class HashTable:

    def __init__(self, size=40):
        self.table = []
        for index in range(size):
            self.table.append([])

    def insert(self, item):
        bucket = hash(item) - 1
        bucket_list = self.table[bucket]
        bucket_list.append(item)

    def search(self, key):
        bucket = hash(key) - 1
        bucket_list = self.table[bucket]
        if key in bucket_list:
            item_index = bucket_list.index(key)
            return bucket_list[item_index]
        else:
            return None

    def remove(self, key):
        bucket = hash(key) - 1
        bucket_list = self.table[bucket]
        if key in bucket_list:
            bucket_list.remove(key)
