# Class that implements a chaining hash table to be used for packages.
class HashTable:
    # Simple constructor for the Hash Table initializes a list of
    # empty lists of the size specified by the parameter.
    def __init__(self, size=40):
        self.table = []
        self.size: size = size
        for index in range(size):
            self.table.append([])

    # Python's built-in __iter__ method allows
    # a HashTable object to be iterable.
    def __iter__(self):
        for bucket in self.table:  # For each bucket in the table...
            for item in bucket:  # and each item in the bucket...
                if item is not None:  # if there is an item in the bucket...
                    yield item  # yield the item over to the iterator.

    # The insert method accepts an item and uses Python's built-in
    # hash function to hash it and place it in the bucket.
    def insert(self, item):
        bucket = hash(item) - 1
        bucket_list = self.table[bucket]
        bucket_list.append(item)

    # The search method accepts the hash key that was used to place the
    # item into the bucket, and uses it to retrieve that item again.
    def search(self, key: int):
        bucket = key - 1
        bucket_list = self.table[bucket]
        for item in bucket_list:
            if hash(item) == key:
                return item

    # The remove method works like the search method, except instead of
    # returning the item it removes it from its bucket within the hash table.
    def remove(self, key: int):
        bucket = key - 1
        bucket_list = self.table[bucket]
        for item in bucket_list:
            if hash(item) == key:
                bucket_list.remove(item)

    # Returns true if all the buckets
    # within the hash table are empty.
    def is_empty(self) -> bool:
        return not any(self.table)

    # Returns true if all the buckets
    # within the hash table are full.
    def is_full(self) -> bool:
        return all(self.table)
